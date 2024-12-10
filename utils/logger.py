import os
import time
import logging

# 创建一个 logger
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)  # 设置日志级别为 DEBUG
# 创建一个 handler，用于写入日志文件
file_dir = './logs'
os.makedirs(file_dir, exist_ok=True)
file_name = f'my_log_{time.strftime("%Y%m%d_%H%M%S")}.log'
file_handler = logging.FileHandler(os.path.join(file_dir, file_name))
file_handler.setLevel(logging.DEBUG)
# 创建一个 formatter，只包含消息内容
formatter = logging.Formatter('%(message)s')
# 添加 formatter 到 handler
file_handler.setFormatter(formatter)
# 添加 handler 到 logger
logger.addHandler(file_handler)

# 记录日志
if __name__ == '__main__':
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')

