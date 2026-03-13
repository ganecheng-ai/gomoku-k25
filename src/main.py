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

# 添加 src 目录到路径
if getattr(sys, 'frozen', False):
    # 打包后的环境
    base_dir = sys._MEIPASS
else:
    # 开发环境
    base_dir = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, base_dir)

# 尝试导入，处理打包后的环境
try:
    from game import main
except ImportError:
    # 打包后的环境，使用绝对导入
    import importlib.util
    game_path = os.path.join(base_dir, 'game.py')
    spec = importlib.util.spec_from_file_location('game', game_path)
    game_module = importlib.util.module_from_spec(spec)
    sys.modules['game'] = game_module
    spec.loader.exec_module(game_module)
    main = game_module.main

if __name__ == "__main__":
    main()
