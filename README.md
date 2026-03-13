# 五子棋 (Gomoku)

一款精美的五子棋游戏，使用 Python + Pygame 开发，支持简体中文界面。

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.5%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 功能特性

- **精美界面**：仿木纹棋盘设计，棋子带立体高光效果
- **标准规则**：15x15 标准棋盘，五子连珠获胜
- **悔棋功能**：支持悔棋操作
- **中文支持**：完整简体中文界面
- **日志系统**：自动记录游戏过程，方便问题定位
- **跨平台**：支持 Windows、Linux、macOS

## 截图

（游戏截图待添加）

## 快速开始

### 下载预编译版本

从 [Releases](https://github.com/ganecheng-ai/gomoku-k25/releases) 页面下载对应系统的版本：

- **Windows**: `gomoku-windows-x64.exe`
- **Linux**: `gomoku-linux-x86_64.tar.gz`
- **macOS**: `gomoku-macos-universal.dmg`

### 从源码运行

#### 环境要求

- Python 3.8 或更高版本
- Pygame 2.5.0 或更高版本

#### 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/ganecheng-ai/gomoku-k25.git
cd gomoku-k25
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 运行游戏：
```bash
python src/main.py
```

## 操作说明

| 操作 | 说明 |
|------|------|
| 左键点击棋盘 | 在当前位置落子 |
| 悔棋按钮 | 撤销上一步操作 |
| 重新开始按钮 | 重新开始一局游戏 |
| 退出按钮 | 退出游戏 |
| ESC 键 | 退出游戏 |
| R 键 | 重新开始 |
| U 键 | 悔棋 |

## 项目结构

```
gomoku-k25/
├── src/                    # 源代码目录
│   ├── __init__.py
│   ├── main.py            # 程序入口
│   ├── game.py            # 游戏主逻辑
│   ├── board.py           # 棋盘类
│   ├── renderer.py        # 渲染器
│   ├── config.py          # 配置文件
│   └── utils.py           # 工具函数（含日志）
├── assets/                 # 资源目录
│   ├── images/
│   └── sounds/
├── tests/                  # 测试目录
├── .github/workflows/      # GitHub Actions 配置
├── requirements.txt        # Python 依赖
├── plan.md                # 开发计划
├── prompt.md              # 项目指令
└── README.md              # 项目说明
```

## 打包

使用 PyInstaller 打包为可执行文件：

```bash
cd src

# Windows
pyinstaller --onefile --windowed --name gomoku --add-data "../assets;assets" main.py

# Linux/macOS
pyinstaller --onefile --windowed --name gomoku --add-data "../assets:assets" main.py
```

## 日志

游戏日志文件保存在程序运行目录的 `logs/` 文件夹中，格式为：
```
gomoku_YYYYMMDD_HHMMSS.log
```

## 更新日志

### v1.0.1 (2025-03-13)

- **亮点介绍**
  - 修复 CI/CD 构建流程
  - 支持 Windows、Linux、macOS 全平台自动构建

- **问题修复**
  - 修复 assets 目录缺失导致构建失败的问题
  - 修复 macOS 构建中 --icon=NONE 参数错误
  - 修复 macOS onefile + windowed 模式冲突

### v1.0.0 (2025-03-13)

- **亮点介绍**
  - 首次发布五子棋游戏
  - 精美的木纹风格界面
  - 完整的悔棋和重新开始功能

- **新增功能**
  - 15x15 标准五子棋棋盘
  - 黑白双方轮流落子
  - 自动胜负判定
  - 悔棋功能
  - 重新开始功能

- **优化改进**
  - 棋子带立体高光效果
  - 最后一步落子位置高亮显示
  - 中文界面支持

- **问题修复**
  - 无（首次发布）

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可

本项目采用 MIT 许可证。

---

**提示**：本项目由 Claude Code 辅助开发。
