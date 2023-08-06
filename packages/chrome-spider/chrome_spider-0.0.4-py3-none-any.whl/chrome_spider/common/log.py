import logging
from chrome_spider.common.config import config

def get_logger(level="INFO"):
    logfile = config.logfile
    # 基本配置
    logger = logging.getLogger(__name__)
    logger.propagate = False
    logger.setLevel(level)
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    # 设置文件句柄 管理输出到日志的格式
    file_handler = logging.FileHandler(logfile, 'a+', encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    # 设置stream句柄 管理输出到控制台的格式
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)
    # logger.handlers.clear()
    # 添加句柄到logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    # file_handler.close()
    # stream_handler.close()
    return logger