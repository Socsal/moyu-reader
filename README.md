# 🐟 摸鱼阅读器 (Moyu Reader)

> **一个透明的桌面阅读器，专为上班摸鱼设计**

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Built by](https://img.shields.io/badge/built%20by-Claude%20(Anthropic)-orange)](https://claude.ai)

## 📖 这是什么？

一个完全透明的桌面小说/电子书阅读器，可以浮在任何窗口上方，让你在上班时优雅地摸鱼。

**特点：**
- ✨ 完全透明 - 可以透过窗口看到后面的工作内容
- 🎯 置顶显示 - 始终浮在最上层
- 📏 可调整大小 - 适应不同的"摸鱼姿势"
- 🔄 双模式 - 自动滚动 / 手动翻页
- 💾 进度保存 - 下次打开继续阅读
- 📚 支持格式 - TXT, EPUB

## 🎬 效果演示

窗口完全透明，文字浮在桌面上，看起来就像在认真工作...

## 🚀 快速开始

### 方式一：直接下载使用（推荐）

1. 下载 [最新版本](https://github.com/shuhao957-dev/moyu-reader/releases)
2. 双击 `设置窗口大小.bat` 设置窗口尺寸
3. 双击 `启动摸鱼阅读器.bat` 开始摸鱼

### 方式二：从源码运行

```bash
# 安装依赖
pip install pywebview ebooklib beautifulsoup4

# 运行
python reader.py
```

## ⌨️ 使用说明

### 快捷键
- **右键点击** - 打开文件
- **空格** - 暂停/继续
- **M** - 切换自动滚动/手动翻页模式
- **↑↓ 方向键** - 手动翻页（手动模式下）
- **滚轮** - 翻页（手动模式下）
- **ESC** - 关闭程序

### 调整窗口大小

1. 运行 `设置窗口大小.bat`
2. 在设置面板中调整宽度和高度
3. 点击"保存设置"
4. 重新启动阅读器，新尺寸生效

💡 **小技巧：** 高度设置为 30-40px 可以完美塞进任务栏上方的缝隙！

## ⚙️ 配置文件

配置文件保存在 `~/.moyu_reader_config.json`：

```json
{
    "window": {
        "width": 400,
        "height": 60,
        "x": 100,
        "y": 100
    },
    "speed": 50
}
```

阅读进度保存在 `~/.moyu_reader_progress.json`。

## 🛠️ 从源码打包

```bash
pyinstaller --onefile --windowed --name "MoyuReader" reader.py
```

**已知问题：** 打包后的 exe 在运行时调整窗口大小会导致透明度失效（这是 pywebview + Windows WebView2 的已知限制）。因此我们采用了独立设置面板的方案。

## 🤝 贡献

欢迎 PR 和 Issue！特别期待：

- [ ] 更好的透明度方案（解决 resize 问题）
- [ ] 更多文件格式支持（PDF, MOBI 等）
- [ ] 更丰富的阅读设置（字体、颜色等）
- [ ] 更隐蔽的"老板键"功能
- [ ] macOS / Linux 支持

## 📜 开发故事

这个项目 **100% 由 AI (Claude by Anthropic) 完成**，人类只负责提需求和测试。

整个开发过程在一次对话中完成，主要挑战是解决 Windows 下 pywebview 透明窗口的各种兼容性问题（踩了无数坑）。

如果你对 AI 辅助编程或 pywebview 开发感兴趣，可以参考这个项目的代码。

## ⚠️ 免责声明

本工具仅供学习交流使用。

请合理安排工作和休息时间，在不影响工作的前提下使用本工具。

作者不对因使用本工具而导致的任何后果负责（比如被老板发现）。😅

## 📄 License

MIT License

---

**⭐ 如果这个小工具帮你成功摸鱼，请给个 Star！**

*Built with ❤️ by Claude (and a hardworking human tester)*
