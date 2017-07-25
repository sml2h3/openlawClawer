#-*- coding:utf-8 -*-
# @Time    : 2017/7/20 12:33
# @Author  : Sml2h3
# @Site    : www.ydyd.me
# @File    : System.py
# @Software: PyCharm
from Config.Config import *
from Logger.Logger import Logger
from Master import Master
from Slaver import Slaver
Logger = Logger('System')


class System(object):
    def __init__(self):
        self.identity = "master"
        self.distributed = True
        self.redis_host = '127.0.0.1'
        self.redis_port = 6379
        self.redis_database = 0
        self.redis_password = ''

    def _run(self):
        if Base['distributed']:
            Logger.info("正在加载程序配置")
            self.__setidentity(Base['identity'])
            self.__setredis_host(Redis['host'])
            self.__setredis_port(Redis['port'])
            self.__setredis_database(Redis['database'])
            self.__setredis_password(Redis['password'])
            Logger.info("************************************************************")
            Logger.info("程序配置加载完毕，信息如下:")
            Logger.info("机器身份:" + "主机" if self.identity == 'master' else '从机')
            Logger.info("Redis Host:" + self.redis_host)
            Logger.info("Redis Port:" + str(self.redis_port))
            Logger.info("Redis Password:" + self.redis_password)
            Logger.info("Redis Database:" + str(self.redis_database))
            Logger.info("************************************************************")
            choice = str(raw_input("请确认以上信息是否正确？（y/n）"))
            if(choice == 'y'):
                self.__work()
            else:
                Logger.info("byebye~")
                exit()
        else:
            Logger.info("此程序尚未开通单机版功能")

    def __setidentity(self, value="master"):
        self.identity = value
        return

    def __setredis_host(self, value="127.0.0.1"):
        self.redis_host = value
        return

    def __setredis_port(self, value=6379):
        self.redis_port = value
        return

    def __setredis_database(self, value=0):
        self.redis_database = value
        return

    def __setredis_password(self, value=''):
        self.redis_password = value
        return

    def __work(self):
        if self.identity == "master":
            Master(self)
        else:
            Slaver(self)