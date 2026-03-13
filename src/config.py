"""
五子棋游戏配置文件
"""

# 窗口设置
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 800
WINDOW_TITLE = "五子棋 (Gomoku)"
FPS = 60

# 棋盘设置
BOARD_SIZE = 15  # 15x15 标准棋盘
MARGIN = 50  # 边距
CELL_SIZE = 50  # 格子大小

# 颜色定义
COLOR_BACKGROUND = (245, 222, 179)  # 暖黄色背景（仿木纹色）
COLOR_BOARD = (222, 184, 135)  # 棋盘颜色
COLOR_LINE = (101, 67, 33)  # 线条颜色（深棕色）
COLOR_BLACK = (30, 30, 30)  # 黑棋颜色
COLOR_WHITE = (250, 250, 250)  # 白棋颜色
COLOR_HIGHLIGHT = (255, 100, 100)  # 高亮颜色
COLOR_TEXT = (50, 50, 50)  # 文字颜色
COLOR_BUTTON_BG = (200, 180, 140)  # 按钮背景色
COLOR_BUTTON_HOVER = (220, 200, 160)  # 按钮悬停色
COLOR_PANEL = (235, 215, 175)  # 面板背景色

# 棋子设置
STONE_RADIUS = 20
STONE_SHADOW_OFFSET = 2

# 游戏状态
STATE_PLAYING = 0
STATE_BLACK_WIN = 1
STATE_WHITE_WIN = 2
STATE_DRAW = 3

# 字体设置
FONT_NAME = "simhei"  # 优先使用黑体
FONT_SIZE_LARGE = 48
FONT_SIZE_MEDIUM = 32
FONT_SIZE_SMALL = 20
