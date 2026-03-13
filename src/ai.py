"""
AI 模块 - 五子棋人机对战

实现基于评估函数和极小化极大算法的 AI
"""

import random
from typing import Optional, Tuple, List

try:
    from .config import BOARD_SIZE
    from .utils import log_debug, log_info
except ImportError:
    from config import BOARD_SIZE
    from utils import log_debug, log_info


class GomokuAI:
    """五子棋 AI 类"""

    # 棋型评分表（从高到低）
    SCORE_FIVE = 1000000           # 连五（必胜）
    SCORE_FOUR = 100000            # 活四（必胜）
    SCORE_FOUR_BLOCKED = 50000     # 冲四（需要阻止）
    SCORE_THREE = 10000            # 活三（有威胁）
    SCORE_THREE_BLOCKED = 1000     # 眠三
    SCORE_TWO = 500                # 活二
    SCORE_TWO_BLOCKED = 50         # 眠二
    SCORE_ONE = 10                 # 活一

    def __init__(self, difficulty: str = "medium"):
        """
        初始化 AI

        Args:
            difficulty: 难度级别 - "easy", "medium", "hard"
        """
        self.difficulty = difficulty
        self.search_depth = self._get_search_depth(difficulty)
        log_info(f"AI 初始化完成，难度: {difficulty}, 搜索深度: {self.search_depth}")

    def _get_search_depth(self, difficulty: str) -> int:
        """根据难度获取搜索深度"""
        depths = {
            "easy": 1,
            "medium": 2,
            "hard": 3
        }
        return depths.get(difficulty, 2)

    def get_move(self, board: List[List[int]], player: int) -> Optional[Tuple[int, int]]:
        """
        获取 AI 的下一步棋

        Args:
            board: 当前棋盘状态
            player: AI 执子颜色 (1=黑, 2=白)

        Returns:
            (row, col) 或 None
        """
        opponent = 3 - player  # 切换玩家

        # 获取候选位置
        candidates = self._get_candidates(board)
        if not candidates:
            # 棋盘为空，下在中心
            center = BOARD_SIZE // 2
            return (center, center)

        log_debug(f"AI 候选位置数量: {len(candidates)}")

        best_score = float('-inf')
        best_moves = []

        for row, col in candidates:
            # 模拟落子
            board[row][col] = player
            score = self._minimax(board, self.search_depth - 1, float('-inf'), float('inf'), False, player, opponent)
            board[row][col] = 0  # 撤销

            log_debug(f"位置 ({row}, {col}) 评分: {score}")

            if score > best_score:
                best_score = score
                best_moves = [(row, col)]
            elif score == best_score:
                best_moves.append((row, col))

        # 从最佳移动中随机选择（增加变化性）
        if best_moves:
            move = random.choice(best_moves)
            log_info(f"AI 选择位置: {move}, 评分: {best_score}")
            return move

        return None

    def _minimax(self, board: List[List[int]], depth: int, alpha: float, beta: float,
                 is_maximizing: bool, ai_player: int, opponent: int) -> float:
        """
        带 Alpha-Beta 剪枝的极小化极大算法

        Args:
            board: 棋盘状态
            depth: 剩余搜索深度
            alpha: 最大值
            beta: 最小值
            is_maximizing: 是否最大化玩家
            ai_player: AI 执子
            opponent: 对手执子

        Returns:
            局面评分
        """
        # 终局判断
        if depth == 0:
            return self._evaluate_board(board, ai_player)

        # 获取候选位置
        candidates = self._get_candidates(board)
        if not candidates:
            return self._evaluate_board(board, ai_player)

        if is_maximizing:
            max_eval = float('-inf')
            for row, col in candidates:
                board[row][col] = ai_player
                if self._check_win(board, row, col, ai_player):
                    board[row][col] = 0
                    return self.SCORE_FIVE * (depth + 1)  # 快速获胜加分
                eval_score = self._minimax(board, depth - 1, alpha, beta, False, ai_player, opponent)
                board[row][col] = 0
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for row, col in candidates:
                board[row][col] = opponent
                if self._check_win(board, row, col, opponent):
                    board[row][col] = 0
                    return -self.SCORE_FIVE * (depth + 1)  # 必须阻止对手获胜
                eval_score = self._minimax(board, depth - 1, alpha, beta, True, ai_player, opponent)
                board[row][col] = 0
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval

    def _get_candidates(self, board: List[List[int]]) -> List[Tuple[int, int]]:
        """
        获取候选落子位置

        策略：只考虑已有棋子周围的位置
        """
        candidates = set()
        has_stone = False

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board[row][col] != 0:
                    has_stone = True
                    # 添加周围空位
                    for dr in range(-2, 3):
                        for dc in range(-2, 3):
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] == 0:
                                candidates.add((nr, nc))

        # 如果棋盘为空，返回中心位置
        if not has_stone:
            center = BOARD_SIZE // 2
            return [(center, center)]

        return list(candidates)

    def _evaluate_board(self, board: List[List[int]], player: int) -> float:
        """
        评估当前局面

        Args:
            board: 棋盘状态
            player: 评估视角的玩家

        Returns:
            局面评分
        """
        score = 0
        opponent = 3 - player

        # 评估所有位置
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board[row][col] == player:
                    score += self._evaluate_position(board, row, col, player)
                elif board[row][col] == opponent:
                    score -= self._evaluate_position(board, row, col, opponent)

        return score

    def _evaluate_position(self, board: List[List[int]], row: int, col: int, player: int) -> float:
        """
        评估某个位置的价值

        评估四个方向的棋型
        """
        if board[row][col] != player:
            return 0

        directions = [
            [(0, 1), (0, -1)],   # 水平
            [(1, 0), (-1, 0)],   # 垂直
            [(1, 1), (-1, -1)],  # 对角线
            [(1, -1), (-1, 1)]   # 反对角线
        ]

        total_score = 0

        for dir_pair in directions:
            count = 1
            empty_ends = 0

            for dr, dc in dir_pair:
                r, c = row + dr, col + dc
                while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                    if board[r][c] == player:
                        count += 1
                        r += dr
                        c += dc
                    elif board[r][c] == 0:
                        empty_ends += 1
                        break
                    else:
                        break

            # 根据棋型评分
            if count >= 5:
                total_score += self.SCORE_FIVE
            elif count == 4:
                if empty_ends == 2:
                    total_score += self.SCORE_FOUR
                elif empty_ends == 1:
                    total_score += self.SCORE_FOUR_BLOCKED
            elif count == 3:
                if empty_ends == 2:
                    total_score += self.SCORE_THREE
                elif empty_ends == 1:
                    total_score += self.SCORE_THREE_BLOCKED
            elif count == 2:
                if empty_ends == 2:
                    total_score += self.SCORE_TWO
                elif empty_ends == 1:
                    total_score += self.SCORE_TWO_BLOCKED
            elif count == 1 and empty_ends == 2:
                total_score += self.SCORE_ONE

        return total_score

    def _check_win(self, board: List[List[int]], row: int, col: int, player: int) -> bool:
        """
        检查是否获胜

        Args:
            board: 棋盘状态
            row: 落子行
            col: 落子列
            player: 玩家

        Returns:
            是否五连
        """
        if board[row][col] != player:
            return False

        directions = [
            [(0, 1), (0, -1)],   # 水平
            [(1, 0), (-1, 0)],   # 垂直
            [(1, 1), (-1, -1)],  # 对角线
            [(1, -1), (-1, 1)]   # 反对角线
        ]

        for dir_pair in directions:
            count = 1
            for dr, dc in dir_pair:
                r, c = row + dr, col + dc
                while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
                    count += 1
                    r += dr
                    c += dc
            if count >= 5:
                return True

        return False
