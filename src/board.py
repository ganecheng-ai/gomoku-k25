"""
棋盘类 - 管理棋盘状态和胜负判定
"""

try:
    from .config import BOARD_SIZE, STATE_BLACK_WIN, STATE_WHITE_WIN, STATE_DRAW, STATE_PLAYING
    from .utils import log_info, log_debug
except ImportError:
    from config import BOARD_SIZE, STATE_BLACK_WIN, STATE_WHITE_WIN, STATE_DRAW, STATE_PLAYING
    from utils import log_info, log_debug

class Board:
    """五子棋棋盘类"""

    # 空位、黑棋、白棋
    EMPTY = 0
    BLACK = 1
    WHITE = 2

    def __init__(self):
        """初始化棋盘"""
        self.size = BOARD_SIZE
        self.reset()
        log_info("棋盘初始化完成")

    def reset(self):
        """重置棋盘"""
        self.board = [[self.EMPTY for _ in range(self.size)] for _ in range(self.size)]
        self.current_player = self.BLACK
        self.move_history = []
        self.state = STATE_PLAYING
        log_info("棋盘已重置")

    def get_board(self):
        """获取当前棋盘状态"""
        return self.board.copy()

    def get_current_player(self):
        """获取当前玩家"""
        return self.current_player

    def get_opponent(self):
        """获取对手"""
        return self.WHITE if self.current_player == self.BLACK else self.BLACK

    def is_valid_move(self, row, col):
        """检查位置是否可落子"""
        if row < 0 or row >= self.size or col < 0 or col >= self.size:
            return False
        return self.board[row][col] == self.EMPTY

    def make_move(self, row, col):
        """
        在指定位置落子

        Args:
            row: 行索引
            col: 列索引

        Returns:
            bool: 落子是否成功
        """
        if not self.is_valid_move(row, col):
            return False

        self.board[row][col] = self.current_player
        self.move_history.append((row, col, self.current_player))
        log_debug(f"落子: 玩家{'黑' if self.current_player == self.BLACK else '白'} 位置({row}, {col})")

        # 检查胜负
        if self.check_win(row, col):
            self.state = STATE_BLACK_WIN if self.current_player == self.BLACK else STATE_WHITE_WIN
            log_info(f"游戏结束: {'黑方' if self.current_player == self.BLACK else '白方'}获胜!")
        elif self.is_full():
            self.state = STATE_DRAW
            log_info("游戏结束: 平局!")
        else:
            # 切换玩家
            self.current_player = self.get_opponent()

        return True

    def undo_move(self):
        """悔棋 - 撤销上一步"""
        if not self.move_history:
            return False

        row, col, player = self.move_history.pop()
        self.board[row][col] = self.EMPTY
        self.current_player = player
        self.state = STATE_PLAYING
        log_info(f"悔棋: 撤销{'黑方' if player == self.BLACK else '白方'}的落子({row}, {col})")
        return True

    def is_full(self):
        """检查棋盘是否已满"""
        return len(self.move_history) == self.size * self.size

    def check_win(self, row, col):
        """
        检查指定位置落子后是否获胜

        Args:
            row: 行索引
            col: 列索引

        Returns:
            bool: 是否获胜
        """
        player = self.board[row][col]
        if player == self.EMPTY:
            return False

        # 四个方向：水平、垂直、对角线、反对角线
        directions = [
            [(0, 1), (0, -1)],   # 水平
            [(1, 0), (-1, 0)],   # 垂直
            [(1, 1), (-1, -1)],  # 对角线
            [(1, -1), (-1, 1)]   # 反对角线
        ]

        for dir_pair in directions:
            count = 1  # 当前落子算1个

            for dr, dc in dir_pair:
                r, c = row + dr, col + dc
                while 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == player:
                    count += 1
                    r += dr
                    c += dc

            if count >= 5:
                return True

        return False

    def get_last_move(self):
        """获取最后一步落子位置"""
        if not self.move_history:
            return None
        return self.move_history[-1][:2]

    def get_move_count(self):
        """获取已落子数量"""
        return len(self.move_history)
