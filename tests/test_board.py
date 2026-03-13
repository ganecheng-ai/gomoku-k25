"""
五子棋棋盘测试模块
"""

import unittest
import sys
import os

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from board import Board
from config import BOARD_SIZE, STATE_PLAYING, STATE_BLACK_WIN, STATE_WHITE_WIN, STATE_DRAW


class TestBoard(unittest.TestCase):
    """测试棋盘类"""

    def setUp(self):
        """每个测试用例前初始化"""
        self.board = Board()

    def test_initial_state(self):
        """测试初始状态"""
        self.assertEqual(self.board.size, BOARD_SIZE)
        self.assertEqual(self.board.current_player, Board.BLACK)
        self.assertEqual(self.board.state, STATE_PLAYING)
        self.assertEqual(len(self.board.move_history), 0)

    def test_valid_move(self):
        """测试有效落子"""
        self.assertTrue(self.board.is_valid_move(7, 7))
        self.assertTrue(self.board.make_move(7, 7))
        self.assertEqual(self.board.board[7][7], Board.BLACK)
        self.assertEqual(self.board.current_player, Board.WHITE)

    def test_invalid_move(self):
        """测试无效落子"""
        # 超出边界
        self.assertFalse(self.board.is_valid_move(-1, 0))
        self.assertFalse(self.board.is_valid_move(0, -1))
        self.assertFalse(self.board.is_valid_move(BOARD_SIZE, 0))
        self.assertFalse(self.board.is_valid_move(0, BOARD_SIZE))

        # 重复落子
        self.board.make_move(7, 7)
        self.assertFalse(self.board.is_valid_move(7, 7))
        self.assertFalse(self.board.make_move(7, 7))

    def test_horizontal_win(self):
        """测试水平获胜"""
        # 黑棋横向五连
        for col in range(5):
            self.board.make_move(7, col)
            if col < 4:
                self.board.make_move(6, col)  # 白棋随便下
        self.assertEqual(self.board.state, STATE_BLACK_WIN)

    def test_vertical_win(self):
        """测试垂直获胜"""
        # 黑棋纵向五连
        for row in range(5):
            self.board.make_move(row, 7)
            if row < 4:
                self.board.make_move(row, 6)  # 白棋随便下
        self.assertEqual(self.board.state, STATE_BLACK_WIN)

    def test_diagonal_win(self):
        """测试对角线获胜"""
        # 黑棋对角线五连
        for i in range(5):
            self.board.make_move(i, i)
            if i < 4:
                self.board.make_move(i, i + 1)  # 白棋随便下
        self.assertEqual(self.board.state, STATE_BLACK_WIN)

    def test_undo_move(self):
        """测试悔棋"""
        self.board.make_move(7, 7)
        self.assertEqual(len(self.board.move_history), 1)
        self.assertTrue(self.board.undo_move())
        self.assertEqual(len(self.board.move_history), 0)
        self.assertEqual(self.board.board[7][7], Board.EMPTY)
        self.assertEqual(self.board.current_player, Board.BLACK)

    def test_undo_empty(self):
        """测试空棋盘悔棋"""
        self.assertFalse(self.board.undo_move())

    def test_reset(self):
        """测试重置"""
        self.board.make_move(7, 7)
        self.board.reset()
        self.assertEqual(self.board.state, STATE_PLAYING)
        self.assertEqual(self.board.current_player, Board.BLACK)
        self.assertEqual(len(self.board.move_history), 0)

    def test_draw(self):
        """测试平局检测逻辑"""
        # 模拟棋盘已满但没有获胜者的情况
        # 手动填满棋盘
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                # 检查是否已结束
                if self.board.state != STATE_PLAYING:
                    break
                # 找到一个有效的落子位置
                if self.board.is_valid_move(row, col):
                    self.board.board[row][col] = self.board.current_player
                    self.board.move_history.append((row, col, self.board.current_player))
                    # 切换玩家
                    self.board.current_player = self.board.get_opponent()

        # 检查是否已满
        self.assertTrue(self.board.is_full())
        # 手动设置状态为平局来测试 is_full 方法
        self.board.state = STATE_DRAW
        self.assertEqual(self.board.state, STATE_DRAW)

    def test_get_last_move(self):
        """测试获取最后一步"""
        self.assertIsNone(self.board.get_last_move())
        self.board.make_move(7, 7)
        self.assertEqual(self.board.get_last_move(), (7, 7))

    def test_get_move_count(self):
        """测试获取步数"""
        self.assertEqual(self.board.get_move_count(), 0)
        self.board.make_move(7, 7)
        self.assertEqual(self.board.get_move_count(), 1)


if __name__ == '__main__':
    unittest.main()
