#-*- coding:utf-8 -*-
# @Time    : 2017/7/21 05:10
# @Author  : Sml2h3
# @Site    : www.ydyd.me
# @File    : Master.py
# @Software: PyCharm
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import redis
from Logger.Logger import Logger
from Login.Login import Login
from Clawer.Clawer import Clawer
Logger = Logger('Master')

class Master(object):
    def __init__(self, config):
        Logger.info("欢迎进入主服务器系统，即将开始进行配置验证")
        self.identity = config.identity
        self.redis_host = config.redis_host
        self.redis_port = config.redis_port
        self.redis_database = config.redis_database
        self.redis_password = config.redis_password
        self.conn = self.__conn_redis()
        Logger.info("配置验证完成，启动主服务器系统")
        self._run()

    def __conn_redis(self):
        try:
            conn = redis.Redis(host=self.redis_host, password=self.redis_password, socket_connect_timeout=3)
            if conn.ping():
                Logger.info("Redis连接正常")
                return conn
            else:
                # 连接失败
                Logger.error("Redis connect failed")
                exit()
        except redis.ConnectionError:
            # 连接失败
            Logger.error("Redis connect failed")
            exit()
        except redis.TimeoutError:
            Logger.error("Redis timeout error")
            exit()

    def _run(self):
        Logger.info("启动主服务器成功")
        Logger.info("开始进行OPENLAW模拟登陆")
        cookies = Login()._run()
        Logger.info("模拟登陆完成，已经获取用户cookies")
        Logger.info("进入爬虫系统")
        Clawer(self, cookies)._run_master()