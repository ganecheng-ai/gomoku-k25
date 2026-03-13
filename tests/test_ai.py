"""
AI 测试模块
"""

import unittest
import sys
import os

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ai import GomokuAI
from board import Board
from config import BOARD_SIZE


class TestAI(unittest.TestCase):
    """测试 AI 类"""

    def setUp(self):
        """每个测试用例前初始化"""
        self.ai = GomokuAI(difficulty="medium")

    def test_initialization(self):
        """测试 AI 初始化"""
        self.assertEqual(self.ai.difficulty, "medium")
        self.assertEqual(self.ai.search_depth, 2)

    def test_difficulty_levels(self):
        """测试不同难度级别"""
        easy_ai = GomokuAI(difficulty="easy")
        self.assertEqual(easy_ai.search_depth, 1)

        hard_ai = GomokuAI(difficulty="hard")
        self.assertEqual(hard_ai.search_depth, 3)

        default_ai = GomokuAI(difficulty="unknown")
        self.assertEqual(default_ai.search_depth, 2)

    def test_get_move_empty_board(self):
        """测试空棋盘时的 AI 落子"""
        board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        move = self.ai.get_move(board, 1)

        # 空棋盘时 AI 应该下在中心
        center = BOARD_SIZE // 2
        self.assertEqual(move, (center, center))

    def test_get_move_valid(self):
        """测试 AI 返回有效落子位置"""
        board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        # 在中心放置一个棋子
        board[7][7] = 1

        move = self.ai.get_move(board, 2)

        # 确保返回的落子位置有效
        self.assertIsNotNone(move)
        row, col = move
        self.assertTrue(0 <= row < BOARD_SIZE)
        self.assertTrue(0 <= col < BOARD_SIZE)
        self.assertEqual(board[row][col], 0)  # 位置应该是空的

    def test_check_win(self):
        """测试获胜检测"""
        board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]

        # 水平五连
        for col in range(5):
            board[7][col] = 1

        self.assertTrue(self.ai._check_win(board, 7, 0, 1))
        self.assertTrue(self.ai._check_win(board, 7, 4, 1))

    def test_evaluate_position(self):
        """测试位置评估"""
        board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]

        # 单个棋子
        board[7][7] = 1
        score = self.ai._evaluate_position(board, 7, 7, 1)
        self.assertGreater(score, 0)

    def test_get_candidates(self):
        """测试候选位置获取"""
        board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]

        # 空棋盘
        candidates = self.ai._get_candidates(board)
        self.assertEqual(len(candidates), 1)  # 只有中心

        # 放置一个棋子
        board[7][7] = 1
        candidates = self.ai._get_candidates(board)
        self.assertGreater(len(candidates), 0)

        # 确保候选位置不包含已有棋子的位置
        for row, col in candidates:
            self.assertEqual(board[row][col], 0)

    def test_ai_blocks_opponent_win(self):
        """测试 AI 阻止对手获胜"""
        board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]

        # 黑棋即将获胜
        board[7][0] = 1
        board[7][1] = 1
        board[7][2] = 1
        board[7][3] = 1

        # AI 执白棋，应该阻止黑棋
        move = self.ai.get_move(board, 2)
        self.assertIsNotNone(move)

        # AI 应该在 (7, 4) 落子
        self.assertEqual(move, (7, 4))

    def test_ai_seeks_win(self):
        """测试 AI 寻求获胜"""
        board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]

        # 白棋即将获胜
        board[7][0] = 2
        board[7][1] = 2
        board[7][2] = 2
        board[7][3] = 2

        # AI 执白棋，应该完成五连
        move = self.ai.get_move(board, 2)
        self.assertEqual(move, (7, 4))


if __name__ == '__main__':
    unittest.main()
