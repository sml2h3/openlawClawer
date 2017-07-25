#-*- coding:utf-8 -*-
# @Time    : 2017/7/21 04:27
# @Author  : Sml2h3
# @Site    : www.ydyd.me
# @File    : Logger.py
# @Software: PyCharm
import logging


class Logger(object):

    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler('/tmp/test.log')

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()

        # 定义handler的输出格式formatter
        formatter = logging.Formatter('%(asctime)s-[ %(name)s ]-%(levelname)s: %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def error(self, msg):
        self.logger.error(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def debug(self, msg):
        self.logger.debug(msg)


if __name__ == "__main__":
    logger = Logger("test")

    logger.debug('logger5 debug message')
    logger.info('logger5 info message')
    logger.warning('logger5 warning message')
    logger.error('logger5 error message')