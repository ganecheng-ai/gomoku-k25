"""
游戏逻辑模块 - 整合游戏流程
"""

import pygame
import time

try:
    from .board import Board
    from .renderer import Renderer
    from .config import *
    from .utils import log_info, log_error
except ImportError:
    from board import Board
    from renderer import Renderer
    from config import *
    from utils import log_info, log_error

class GomokuGame:
    """五子棋游戏主类"""

    def __init__(self):
        """初始化游戏"""
        log_info("初始化五子棋游戏...")

        # 初始化 Pygame
        pygame.init()
        pygame.display.set_caption(WINDOW_TITLE)

        # 创建窗口
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        # 创建棋盘和渲染器
        self.board = Board()
        self.renderer = Renderer(self.screen)

        # 游戏状态
        self.running = True
        self.game_over = False

        # 计时器
        self.start_time = time.time()
        self.elapsed_time = 0
        self.timer_running = True

        log_info("五子棋游戏初始化完成")

    def run(self):
        """运行游戏主循环"""
        log_info("游戏主循环开始")

        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)

        log_info("游戏主循环结束")
        pygame.quit()

    def handle_events(self):
        """处理输入事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                log_info("用户关闭窗口")

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键点击
                    self.handle_mouse_click(event.pos)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    log_info("用户按ESC键退出")
                elif event.key == pygame.K_r:
                    self.restart_game()
                elif event.key == pygame.K_u:
                    self.undo_move()

    def handle_mouse_click(self, pos):
        """处理鼠标点击"""
        x, y = pos

        # 检查按钮点击
        button = self.renderer.get_button_clicked(x, y)
        if button == 'undo':
            self.undo_move()
            return
        elif button == 'restart':
            self.restart_game()
            return
        elif button == 'quit':
            self.running = False
            log_info("用户点击退出按钮")
            return

        # 如果游戏已结束，点击重新开始
        if self.game_over:
            self.restart_game()
            return

        # 检查是否在棋盘内
        if self.renderer.is_on_board(x, y):
            row, col = self.renderer.to_board_pos(x, y)
            if self.board.is_valid_move(row, col):
                self.make_move(row, col)

    def make_move(self, row, col):
        """在指定位置落子"""
        if self.board.make_move(row, col):
            # 播放落子音效
            self.renderer.play_sound('place')
            if self.board.state != STATE_PLAYING:
                self.game_over = True
                self.timer_running = False
                self.renderer.play_sound('win')
                log_info(f"游戏结束，状态: {self.board.state}")

    def undo_move(self):
        """悔棋"""
        if self.board.undo_move():
            self.game_over = False
            self.timer_running = True
            log_info("悔棋成功")

    def restart_game(self):
        """重新开始游戏"""
        self.board.reset()
        self.game_over = False
        self.start_time = time.time()
        self.elapsed_time = 0
        self.timer_running = True
        log_info("重新开始游戏")

    def update(self):
        """更新游戏状态"""
        if self.timer_running:
            self.elapsed_time = time.time() - self.start_time

    def render(self):
        """渲染游戏画面"""
        # 绘制棋盘
        self.renderer.draw_board()

        # 绘制棋子
        self.renderer.draw_pieces(self.board.get_board(), self.board.get_last_move())

        # 绘制UI（包含计时器）
        self.renderer.draw_ui(
            self.board.get_current_player(),
            self.board.state,
            self.board.get_move_count(),
            self.elapsed_time
        )

        # 绘制按钮
        self.renderer.draw_buttons()

        # 如果游戏结束，绘制覆盖层
        if self.game_over:
            winner = None
            if self.board.state == STATE_BLACK_WIN:
                winner = 1
            elif self.board.state == STATE_WHITE_WIN:
                winner = 2
            else:
                winner = 0
            self.renderer.draw_winner_overlay(winner)

        # 更新显示
        pygame.display.flip()

def main():
    """游戏入口函数"""
    try:
        game = GomokuGame()
        game.run()
    except Exception as e:
        log_error(f"游戏运行时错误: {e}")
        raise

if __name__ == "__main__":
    main()
