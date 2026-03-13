"""
渲染器模块 - 负责绘制游戏界面
"""

import pygame
import os
import math
import array

try:
    from .config import *
    from .utils import log_info
except ImportError:
    from config import *
    from utils import log_info

class Renderer:
    """游戏渲染器类"""

    def __init__(self, screen):
        """初始化渲染器"""
        self.screen = screen
        self.board_offset_x = MARGIN
        self.board_offset_y = MARGIN + 80  # 预留上方空间给状态显示
        self.board_width = (BOARD_SIZE - 1) * CELL_SIZE
        self.board_height = (BOARD_SIZE - 1) * CELL_SIZE

        # 初始化字体
        self.init_fonts()

        # 加载音效
        self.load_sounds()

        log_info("渲染器初始化完成")

    def init_fonts(self):
        """初始化字体"""
        try:
            # 尝试加载系统中文字体
            chinese_fonts = [
                "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",  # Linux 文泉驿
                "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
                "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",  # Noto
                "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
                "/System/Library/Fonts/PingFang.ttc",  # macOS
                "C:\\Windows\\Fonts\\simhei.ttf",  # Windows 黑体
                "C:\\Windows\\Fonts\\simsun.ttc",  # Windows 宋体
                "C:\\Windows\\Fonts\\msyh.ttc",  # Windows 雅黑
            ]

            font_loaded = False
            for font_path in chinese_fonts:
                if os.path.exists(font_path):
                    self.font_large = pygame.font.Font(font_path, FONT_SIZE_LARGE)
                    self.font_medium = pygame.font.Font(font_path, FONT_SIZE_MEDIUM)
                    self.font_small = pygame.font.Font(font_path, FONT_SIZE_SMALL)
                    font_loaded = True
                    log_info(f"加载字体: {font_path}")
                    break

            if not font_loaded:
                # 使用系统默认字体
                self.font_large = pygame.font.SysFont(None, FONT_SIZE_LARGE)
                self.font_medium = pygame.font.SysFont(None, FONT_SIZE_MEDIUM)
                self.font_small = pygame.font.SysFont(None, FONT_SIZE_SMALL)
                log_info("使用系统默认字体")

        except Exception as e:
            self.font_large = pygame.font.SysFont(None, FONT_SIZE_LARGE)
            self.font_medium = pygame.font.SysFont(None, FONT_SIZE_MEDIUM)
            self.font_small = pygame.font.SysFont(None, FONT_SIZE_SMALL)
            log_info(f"字体加载失败，使用默认字体: {e}")

    def load_sounds(self):
        """加载音效"""
        self.sounds = {}
        try:
            pygame.mixer.init()
            # 使用程序生成简单音效，避免依赖外部文件
            self.sounds['place'] = self._generate_place_sound()
            self.sounds['win'] = self._generate_win_sound()
            log_info("音效系统初始化完成")
        except Exception as e:
            log_info(f"音效系统初始化失败: {e}")

    def _generate_place_sound(self):
        """生成落子音效"""
        try:
            # 创建一个短暂的点击音效
            sample_rate = 44100
            duration = 0.1  # 100ms
            frequency = 800  # Hz
            samples = []
            for i in range(int(sample_rate * duration)):
                # 衰减正弦波
                decay = 1 - (i / (sample_rate * duration))
                value = int(8000 * decay * math.sin(2 * math.pi * frequency * i / sample_rate))
                samples.append(value)
            # 转换为 pygame Sound
            sound_buffer = array.array('h', samples).tobytes()
            return pygame.mixer.Sound(buffer=sound_buffer)
        except Exception:
            return None

    def _generate_win_sound(self):
        """生成胜利音效"""
        try:
            sample_rate = 44100
            duration = 0.3
            samples = []
            # 三个音调组成胜利音效
            for freq in [523, 659, 784]:  # C5, E5, G5
                for i in range(int(sample_rate * duration / 3)):
                    decay = 1 - (i / (sample_rate * duration / 3))
                    value = int(10000 * decay * math.sin(2 * math.pi * freq * i / sample_rate))
                    samples.append(value)
            sound_buffer = array.array('h', samples).tobytes()
            return pygame.mixer.Sound(buffer=sound_buffer)
        except Exception:
            return None

    def play_sound(self, sound_name):
        """播放指定音效"""
        if sound_name in self.sounds and self.sounds[sound_name]:
            try:
                self.sounds[sound_name].play()
            except Exception:
                pass

    def to_screen_pos(self, row, col):
        """将棋盘坐标转换为屏幕坐标"""
        x = self.board_offset_x + col * CELL_SIZE
        y = self.board_offset_y + row * CELL_SIZE
        return (x, y)

    def to_board_pos(self, x, y):
        """将屏幕坐标转换为棋盘坐标"""
        col = round((x - self.board_offset_x) / CELL_SIZE)
        row = round((y - self.board_offset_y) / CELL_SIZE)
        return (row, col)

    def draw_board(self):
        """绘制棋盘"""
        # 绘制背景
        self.screen.fill(COLOR_BACKGROUND)

        # 绘制棋盘区域
        board_rect = pygame.Rect(
            self.board_offset_x - 20,
            self.board_offset_y - 20,
            self.board_width + 40,
            self.board_height + 40
        )
        pygame.draw.rect(self.screen, COLOR_BOARD, board_rect, border_radius=10)
        pygame.draw.rect(self.screen, COLOR_LINE, board_rect, 3, border_radius=10)

        # 绘制网格线
        for i in range(BOARD_SIZE):
            # 横线
            start_pos = self.to_screen_pos(i, 0)
            end_pos = self.to_screen_pos(i, BOARD_SIZE - 1)
            pygame.draw.line(self.screen, COLOR_LINE, start_pos, end_pos, 2)

            # 竖线
            start_pos = self.to_screen_pos(0, i)
            end_pos = self.to_screen_pos(BOARD_SIZE - 1, i)
            pygame.draw.line(self.screen, COLOR_LINE, start_pos, end_pos, 2)

        # 绘制星位（天元及四角星）
        star_points = [
            (3, 3), (3, 11), (7, 7), (11, 3), (11, 11)
        ]
        for row, col in star_points:
            pos = self.to_screen_pos(row, col)
            pygame.draw.circle(self.screen, COLOR_LINE, pos, 5)

    def draw_stone(self, row, col, stone_type, is_last=False):
        """绘制棋子"""
        x, y = self.to_screen_pos(row, col)

        # 绘制阴影
        shadow_pos = (x + STONE_SHADOW_OFFSET, y + STONE_SHADOW_OFFSET)
        pygame.draw.circle(self.screen, (100, 100, 100), shadow_pos, STONE_RADIUS)

        # 棋子颜色
        if stone_type == 1:  # 黑棋
            color = COLOR_BLACK
            # 黑棋高光
            highlight_color = (80, 80, 80)
        else:  # 白棋
            color = COLOR_WHITE
            # 白棋阴影
            highlight_color = (230, 230, 230)

        # 绘制棋子主体
        pygame.draw.circle(self.screen, color, (x, y), STONE_RADIUS)

        # 绘制棋子立体感（高光）
        highlight_pos = (x - 5, y - 5)
        pygame.draw.circle(self.screen, highlight_color, highlight_pos, STONE_RADIUS // 3)

        # 标记最后一步
        if is_last:
            if stone_type == 1:
                mark_color = COLOR_WHITE
            else:
                mark_color = COLOR_BLACK
            pygame.draw.circle(self.screen, mark_color, (x, y), 5)

    def draw_pieces(self, board, last_move=None):
        """绘制所有棋子"""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board[row][col] != 0:
                    is_last = (last_move == (row, col))
                    self.draw_stone(row, col, board[row][col], is_last)

    def draw_ui(self, current_player, state, move_count, elapsed_time=0):
        """绘制UI界面"""
        # 绘制顶部面板
        panel_rect = pygame.Rect(0, 0, WINDOW_WIDTH, 70)
        pygame.draw.rect(self.screen, COLOR_PANEL, panel_rect)
        pygame.draw.line(self.screen, COLOR_LINE, (0, 70), (WINDOW_WIDTH, 70), 2)

        # 当前玩家显示
        if state == STATE_PLAYING:
            player_text = f"当前玩家: {'黑棋' if current_player == 1 else '白棋'}"
            player_color = COLOR_BLACK if current_player == 1 else COLOR_WHITE
        elif state == STATE_BLACK_WIN:
            player_text = "黑方获胜!"
            player_color = (200, 0, 0)
        elif state == STATE_WHITE_WIN:
            player_text = "白方获胜!"
            player_color = (200, 0, 0)
        else:
            player_text = "平局!"
            player_color = (100, 100, 100)

        # 格式化时间显示
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        time_text = f"时间: {minutes:02d}:{seconds:02d}"

        # 渲染文字
        title_surface = self.font_medium.render("五子棋", True, COLOR_TEXT)
        self.screen.blit(title_surface, (20, 15))

        status_surface = self.font_small.render(player_text, True, player_color)
        self.screen.blit(status_surface, (200, 20))

        # 步数显示
        step_text = f"步数: {move_count}"
        step_surface = self.font_small.render(step_text, True, COLOR_TEXT)
        self.screen.blit(step_surface, (450, 20))

        # 时间显示
        time_surface = self.font_small.render(time_text, True, COLOR_TEXT)
        self.screen.blit(time_surface, (600, 20))

    def draw_buttons(self):
        """绘制按钮"""
        button_height = 40
        button_y = WINDOW_HEIGHT - 60

        # 悔棋按钮
        self.undo_btn_rect = pygame.Rect(150, button_y, 100, button_height)
        self._draw_button(self.undo_btn_rect, "悔棋", COLOR_BUTTON_BG)

        # 重新开始按钮
        self.restart_btn_rect = pygame.Rect(300, button_y, 120, button_height)
        self._draw_button(self.restart_btn_rect, "重新开始", COLOR_BUTTON_BG)

        # 退出按钮
        self.quit_btn_rect = pygame.Rect(500, button_y, 100, button_height)
        self._draw_button(self.quit_btn_rect, "退出", COLOR_BUTTON_BG)

    def _draw_button(self, rect, text, color):
        """绘制单个按钮"""
        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos):
            color = COLOR_BUTTON_HOVER

        pygame.draw.rect(self.screen, color, rect, border_radius=8)
        pygame.draw.rect(self.screen, COLOR_LINE, rect, 2, border_radius=8)

        text_surface = self.font_small.render(text, True, COLOR_TEXT)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_winner_overlay(self, winner):
        """绘制获胜覆盖层"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        if winner == 1:
            text = "黑方获胜!"
            color = (255, 255, 255)
        elif winner == 2:
            text = "白方获胜!"
            color = (255, 255, 255)
        else:
            text = "平局!"
            color = (200, 200, 200)

        text_surface = self.font_large.render(text, True, color)
        text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        self.screen.blit(text_surface, text_rect)

        # 提示信息
        hint_surface = self.font_small.render("点击鼠标继续游戏", True, (200, 200, 200))
        hint_rect = hint_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
        self.screen.blit(hint_surface, hint_rect)

    def is_on_board(self, x, y):
        """检查坐标是否在棋盘区域内"""
        min_x = self.board_offset_x - CELL_SIZE // 2
        max_x = self.board_offset_x + (BOARD_SIZE - 1) * CELL_SIZE + CELL_SIZE // 2
        min_y = self.board_offset_y - CELL_SIZE // 2
        max_y = self.board_offset_y + (BOARD_SIZE - 1) * CELL_SIZE + CELL_SIZE // 2
        return min_x <= x <= max_x and min_y <= y <= max_y

    def get_button_clicked(self, x, y):
        """获取被点击的按钮"""
        if hasattr(self, 'undo_btn_rect') and self.undo_btn_rect.collidepoint(x, y):
            return 'undo'
        if hasattr(self, 'restart_btn_rect') and self.restart_btn_rect.collidepoint(x, y):
            return 'restart'
        if hasattr(self, 'quit_btn_rect') and self.quit_btn_rect.collidepoint(x, y):
            return 'quit'
        return None
