#-*- coding:utf-8 -*-
# @Time    : 2017/7/20 12:23
# @Author  : Sml2h3
# @Site    : www.ydyd.me
# @File    : Config.py
# @Software: PyCharm

Base = {
    'distributed': True, #是否开始分布式
    'identity': 'master', #identity 身份:master主机slaver从机
}

Redis = {
    'host': 'r-2ze7441de5149074.redis.rds.aliyuncs.com',
    'password': 'CSDNb405',
    'port': 6379, #默认端口
    'database': 0 #默认数据库
}