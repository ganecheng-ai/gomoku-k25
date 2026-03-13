"""
工具函数模块 - 包含日志系统
"""

import os
import sys
import logging
from datetime import datetime

# 获取程序运行目录
def get_app_dir():
    """获取程序运行目录"""
    if getattr(sys, 'frozen', False):
        # 打包后的程序
        return os.path.dirname(sys.executable)
    else:
        # 开发环境
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 日志目录和文件
LOG_DIR = os.path.join(get_app_dir(), "logs")
LOG_FILE = os.path.join(LOG_DIR, f"gomoku_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

# 确保日志目录存在
os.makedirs(LOG_DIR, exist_ok=True)

# 配置日志系统
def setup_logging():
    """设置日志系统"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

# 初始化日志
logger = setup_logging()

def log_info(message):
    """记录信息日志"""
    logger.info(message)

def log_error(message):
    """记录错误日志"""
    logger.error(message)

def log_warning(message):
    """记录警告日志"""
    logger.warning(message)

def log_debug(message):
    """记录调试日志"""
    logger.debug(message)

# 获取资源路径（兼容打包后）
def get_resource_path(relative_path):
    """获取资源文件的绝对路径，兼容开发和打包环境"""
    if getattr(sys, 'frozen', False):
        # 打包后的程序
        base_path = sys._MEIPASS
    else:
        # 开发环境
        base_path = get_app_dir()
    return os.path.join(base_path, relative_path)
