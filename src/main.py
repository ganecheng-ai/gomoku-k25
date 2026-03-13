#!/usr/bin/env python3
"""
五子棋 (Gomoku) - 主程序入口

一个精美的五子棋游戏，支持中文界面。

运行方式:
    python src/main.py

打包方式:
    pyinstaller --onefile --windowed --name gomoku src/main.py
"""

import sys
import os

# 添加当前目录到路径（兼容开发和打包环境）
if getattr(sys, 'frozen', False):
    # 打包后的环境 - PyInstaller 的临时目录
    base_dir = sys._MEIPASS
else:
    # 开发环境
    base_dir = os.path.dirname(os.path.abspath(__file__))

if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

# 导入游戏主函数
from game import main

if __name__ == "__main__":
    main()
