"""
游戏配置测试模块
"""

import unittest
import sys
import os

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config import *


class TestConfig(unittest.TestCase):
    """测试配置文件"""

    def test_window_config(self):
        """测试窗口配置"""
        self.assertIsInstance(WINDOW_WIDTH, int)
        self.assertIsInstance(WINDOW_HEIGHT, int)
        self.assertIsInstance(WINDOW_TITLE, str)
        self.assertIsInstance(FPS, int)
        self.assertGreater(WINDOW_WIDTH, 0)
        self.assertGreater(WINDOW_HEIGHT, 0)
        self.assertGreater(FPS, 0)

    def test_board_config(self):
        """测试棋盘配置"""
        self.assertIsInstance(BOARD_SIZE, int)
        self.assertIsInstance(MARGIN, int)
        self.assertIsInstance(CELL_SIZE, int)
        self.assertEqual(BOARD_SIZE, 15)
        self.assertGreater(MARGIN, 0)
        self.assertGreater(CELL_SIZE, 0)

    def test_colors(self):
        """测试颜色配置"""
        colors = [
            COLOR_BACKGROUND, COLOR_BOARD, COLOR_LINE,
            COLOR_BLACK, COLOR_WHITE, COLOR_HIGHLIGHT,
            COLOR_TEXT, COLOR_BUTTON_BG, COLOR_BUTTON_HOVER, COLOR_PANEL
        ]
        for color in colors:
            self.assertIsInstance(color, tuple)
            self.assertEqual(len(color), 3)
            for c in color:
                self.assertIsInstance(c, int)
                self.assertGreaterEqual(c, 0)
                self.assertLessEqual(c, 255)

    def test_game_states(self):
        """测试游戏状态"""
        self.assertEqual(STATE_PLAYING, 0)
        self.assertEqual(STATE_BLACK_WIN, 1)
        self.assertEqual(STATE_WHITE_WIN, 2)
        self.assertEqual(STATE_DRAW, 3)


if __name__ == '__main__':
    unittest.main()
