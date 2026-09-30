"""Live Windows/WebView2 regression check; run on an unlocked desktop.

Uses the real reader window over a solid-color native window. Pixel samples
must follow that window's color, so checking CSS alpha alone cannot pass.
No books or user configuration are loaded. Only project dependencies are used.
"""

import json
import re
import sys
import time
import traceback
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import webview
import reader
import settings


def main():
    if sys.platform != 'win32':
        raise SystemExit('This check requires Windows and an unlocked desktop.')

    api = SimpleNamespace(config={
        'window': {'width': 400, 'height': 60, 'x': 100, 'y': 100},
        'speed': 50,
    })
    window = reader.create_reader_window(api)
    backdrop = None
    failures = []
    background = (17, 201, 127)

    def on_ui(callback):
        from System import Action
        window.native.Invoke(Action(callback))

    def pixels():
        from System.Drawing import Bitmap, Graphics, Size

        rectangle = []
        on_ui(lambda: rectangle.append(
            window.native.RectangleToScreen(window.native.ClientRectangle)
        ))
        rect = rectangle[0]
        bitmap = Bitmap(1, 1)
        graphics = Graphics.FromImage(bitmap)
        try:
            values = []
            for fraction in (0.1, 0.5, 0.9):
                graphics.CopyFromScreen(
                    rect.Left + int(rect.Width * fraction),
                    rect.Top + int(rect.Height * 0.8), 0, 0, Size(1, 1)
                )
                color = bitmap.GetPixel(0, 0)
                values.append((color.R, color.G, color.B))
            return values
        finally:
            graphics.Dispose()
            bitmap.Dispose()

    def expect_transparent(label):
        # Allow WebView2/DWM to present the new frame, then check actual pixels.
        time.sleep(0.3)
        deadline = time.monotonic() + 2
        actual = pixels()
        while actual != [background] * 3 and time.monotonic() < deadline:
            time.sleep(0.1)
            actual = pixels()
        if actual != [background] * 3:
            raise AssertionError(f'{label}: expected {background}, got {actual}')
        print(f'PASS {label}', flush=True)

    def expect_mouse_target():
        import ctypes
        from ctypes import wintypes

        user32 = ctypes.WinDLL('user32')
        user32.WindowFromPoint.argtypes = [wintypes.POINT]
        user32.WindowFromPoint.restype = wintypes.HWND
        user32.GetAncestor.argtypes = [wintypes.HWND, wintypes.UINT]
        user32.GetAncestor.restype = wintypes.HWND
        state = []
        def read():
            rect = window.native.RectangleToScreen(window.native.ClientRectangle)
            state.append((window.native.Handle.ToInt64(), rect.Left, rect.Top))
        on_ui(read)
        handle, left, top = state[0]
        for x, y in ((12, 12), (200, 80)):
            target = user32.WindowFromPoint(wintypes.POINT(left + x, top + y))
            if user32.GetAncestor(target, 2) != handle:  # GA_ROOT
                raise AssertionError('Reader became click-through to the window behind it.')
        print('PASS native mouse targets text and transparent area', flush=True)

    def run():
        nonlocal backdrop, background
        try:
            if not window.events.loaded.wait(20):
                raise RuntimeError('Reader did not load within 20 seconds.')
            if webview.renderer != 'edgechromium':
                raise RuntimeError('Install Microsoft Edge WebView2 Runtime first.')

            def create_backdrop():
                nonlocal backdrop
                from System.Drawing import Color, Point, Size
                from System.Windows.Forms import Form, FormBorderStyle, FormStartPosition

                backdrop = Form()
                backdrop.Text = 'Moyu transparency test backdrop'
                backdrop.FormBorderStyle = getattr(FormBorderStyle, 'None')
                backdrop.StartPosition = FormStartPosition.Manual
                backdrop.Location = Point(80, 80)
                backdrop.Size = Size(1000, 750)
                backdrop.BackColor = Color.FromArgb(*background)
                backdrop.ShowInTaskbar = False
                backdrop.TopMost = True
                backdrop.Show()
                window.native.BringToFront()

            on_ui(create_backdrop)
            expect_transparent('startup')
            window.resize(600, 120)
            expect_transparent('resize larger')
            window.resize(400, 60)
            expect_transparent('resize smaller')
            window.minimize()
            time.sleep(0.3)
            window.restore()
            expect_transparent('minimize and restore')
            window.move(140, 140)
            expect_transparent('move')
            window.hide()
            time.sleep(0.2)
            window.show()
            expect_transparent('hide and show')

            # Prove that we see the live window behind, not stale painted pixels.
            background = (42, 110, 213)
            def recolor():
                from System.Drawing import Color
                backdrop.BackColor = Color.FromArgb(*background)
                backdrop.Refresh()
            on_ui(recolor)
            expect_transparent('background changes behind reader')

            settings_html = settings.get_html()
            css = re.search(r'<style>(.*?)</style>', settings_html, re.S).group(1)
            panel = re.search(r'<body[^>]*>(.*?)<script>', settings_html, re.S).group(1)
            window.evaluate_js('''(() => {
                const style = document.createElement('style');
                style.textContent = %s;
                document.head.appendChild(style);
                document.body.insertAdjacentHTML('beforeend', %s);
                const panel = document.getElementById('moyu-settings');
                panel.style.cssText = 'position:fixed;inset:0;z-index:2000;overflow:auto;display:none';
            })()''' % (json.dumps(css), json.dumps(panel)))
            expect_transparent('settings CSS loaded, panel hidden')
            body_style = window.evaluate_js('''({
                color: getComputedStyle(document.body).backgroundColor,
                image: getComputedStyle(document.body).backgroundImage
            })''')
            if body_style != {'color': 'rgba(0, 0, 0, 0)', 'image': 'none'}:
                raise AssertionError(f'Settings changed the reader background: {body_style}')

            window.resize(600, 600)
            window.evaluate_js("document.getElementById('moyu-settings').style.display = 'block'")
            time.sleep(0.5)
            if pixels() == [background] * 3:
                raise AssertionError('The visible settings panel should paint its own background.')
            print('PASS settings panel paints its own background', flush=True)
            window.evaluate_js("document.getElementById('moyu-settings').style.display = 'none'")
            window.resize(400, 60)
            expect_transparent('close settings and restore reader size')
            window.minimize()
            time.sleep(0.3)
            window.restore()
            expect_transparent('restore with settings CSS still loaded')
            expect_mouse_target()

            # Keep the reader's own controls functional after settings CSS loads.
            mode = window.evaluate_js("document.getElementById('mode-btn').click(); document.getElementById('mode-btn').textContent")
            if mode != '手动':
                raise AssertionError(f'Reader mode control stopped working: {mode}')
            print('PASS reader controls after loading settings CSS', flush=True)
        except Exception:
            failures.append(traceback.format_exc())
        finally:
            try:
                if backdrop is not None:
                    on_ui(backdrop.Close)
            finally:
                window.destroy()

    webview.start(run)
    if failures:
        raise SystemExit('\n'.join(failures))
    print('All Windows transparency checks passed.')


if __name__ == '__main__':
    main()
