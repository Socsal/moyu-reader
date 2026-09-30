import webview
import json
from pathlib import Path


class Settings:
    def __init__(self):
        self.config_file = Path.home() / '.moyu_reader_config.json'
        self.load_config()

    def load_config(self):
        """加载配置文件"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                self.config = {
                    'window': {'width': 400, 'height': 60, 'x': 100, 'y': 100},
                    'speed': 50
                }
        except:
            self.config = {
                'window': {'width': 400, 'height': 60, 'x': 100, 'y': 100},
                'speed': 50
            }

    def save_config(self):
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            return {'success': True, 'message': '设置已保存！'}
        except Exception as e:
            return {'success': False, 'message': f'保存失败：{str(e)}'}

    def get_config(self):
        """获取当前配置"""
        return self.config

    def update_window_size(self, width, height):
        """更新窗口大小"""
        self.config['window']['width'] = width
        self.config['window']['height'] = height
        return self.save_config()

    def update_speed(self, speed):
        """更新速度"""
        self.config['speed'] = speed
        return self.save_config()


def get_html():
    """返回设置面板HTML内容"""
    return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        #moyu-settings, #moyu-settings * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        #moyu-settings {
            font-family: "Microsoft YaHei", sans-serif;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }

        #moyu-settings .container {
            max-width: 500px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }

        #moyu-settings h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
            font-size: 24px;
        }

        #moyu-settings .setting-group {
            margin-bottom: 25px;
            padding-bottom: 20px;
            border-bottom: 1px solid #eee;
        }

        #moyu-settings .setting-group:last-child {
            border-bottom: none;
        }

        #moyu-settings label {
            display: block;
            font-size: 14px;
            color: #666;
            margin-bottom: 8px;
            font-weight: bold;
        }

        #moyu-settings .input-group {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        #moyu-settings input[type="number"] {
            flex: 1;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 6px;
            font-size: 16px;
            transition: border-color 0.3s;
        }

        #moyu-settings input[type="number"]:focus {
            outline: none;
            border-color: #667eea;
        }

        #moyu-settings .unit {
            color: #999;
            font-size: 14px;
        }

        #moyu-settings .current-value {
            color: #667eea;
            font-weight: bold;
            font-size: 18px;
        }

        #moyu-settings button {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            margin-top: 10px;
        }

        #moyu-settings button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        #moyu-settings button:active {
            transform: translateY(0);
        }

        #moyu-settings .message {
            margin-top: 15px;
            padding: 12px;
            border-radius: 6px;
            text-align: center;
            font-size: 14px;
            display: none;
        }

        #moyu-settings .message.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }

        #moyu-settings .message.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }

        #moyu-settings .preset-buttons {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
            margin-top: 10px;
        }

        #moyu-settings .preset-btn {
            padding: 8px;
            background: #f0f0f0;
            border: 1px solid #ddd;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            transition: all 0.2s;
        }

        #moyu-settings .preset-btn:hover {
            background: #e0e0e0;
            border-color: #999;
        }

        #moyu-settings .info-text {
            font-size: 12px;
            color: #999;
            margin-top: 5px;
            line-height: 1.5;
        }
    </style>
</head>
<body style="margin: 0;">
  <div id="moyu-settings">
    <div class="container">
        <h1>📐 摸鱼阅读器 - 窗口设置</h1>

        <div class="setting-group">
            <label>窗口宽度</label>
            <div class="input-group">
                <input type="number" id="width" min="150" max="1200" value="400">
                <span class="unit">px</span>
            </div>
            <div class="preset-buttons">
                <button class="preset-btn" onclick="setWidth(200)">窄 (200)</button>
                <button class="preset-btn" onclick="setWidth(400)">中 (400)</button>
                <button class="preset-btn" onclick="setWidth(600)">宽 (600)</button>
            </div>
        </div>

        <div class="setting-group">
            <label>窗口高度</label>
            <div class="input-group">
                <input type="number" id="height" min="20" max="600" value="60">
                <span class="unit">px</span>
            </div>
            <div class="preset-buttons">
                <button class="preset-btn" onclick="setHeight(30)">一行 (30)</button>
                <button class="preset-btn" onclick="setHeight(60)">两行 (60)</button>
                <button class="preset-btn" onclick="setHeight(120)">多行 (120)</button>
            </div>
            <div class="info-text">💡 提示：设置高度为 30-40 可以完美塞进任务栏缝隙</div>
        </div>

        <div class="setting-group">
            <label>默认滚动速度</label>
            <div class="input-group">
                <input type="number" id="speed" min="10" max="200" value="50">
                <span class="current-value" id="speed-display">50</span>
            </div>
        </div>

        <button onclick="saveSettings()">💾 保存设置</button>
        <div id="message" class="message"></div>

        <div class="info-text" style="margin-top: 20px; text-align: center;">
            ⚠️ 修改设置后，需要重新启动阅读器才能生效
        </div>
    </div>
  </div>

    <script>
        // 页面加载时获取当前配置
        window.addEventListener('DOMContentLoaded', async () => {
            const config = await pywebview.api.get_config();
            document.getElementById('width').value = config.window.width;
            document.getElementById('height').value = config.window.height;
            document.getElementById('speed').value = config.speed;
            document.getElementById('speed-display').textContent = config.speed;
        });

        // 监听速度输入变化
        document.getElementById('speed').addEventListener('input', (e) => {
            document.getElementById('speed-display').textContent = e.target.value;
        });

        function setWidth(value) {
            document.getElementById('width').value = value;
        }

        function setHeight(value) {
            document.getElementById('height').value = value;
        }

        async function saveSettings() {
            const width = parseInt(document.getElementById('width').value);
            const height = parseInt(document.getElementById('height').value);
            const speed = parseInt(document.getElementById('speed').value);

            // 保存窗口大小
            const result1 = await pywebview.api.update_window_size(width, height);

            // 保存速度
            const result2 = await pywebview.api.update_speed(speed);

            // 显示消息
            const messageDiv = document.getElementById('message');
            if (result1.success && result2.success) {
                messageDiv.className = 'message success';
                messageDiv.textContent = '✅ ' + result1.message;
            } else {
                messageDiv.className = 'message error';
                messageDiv.textContent = '❌ ' + (result1.message || result2.message);
            }
            messageDiv.style.display = 'block';

            // 3秒后隐藏消息
            setTimeout(() => {
                messageDiv.style.display = 'none';
            }, 3000);
        }
    </script>
</body>
</html>
    """


if __name__ == '__main__':
    api = Settings()

    window = webview.create_window(
        '摸鱼阅读器 - 设置',
        html=get_html(),
        js_api=api,
        width=550,
        height=600,
        resizable=False
    )

    webview.start()
