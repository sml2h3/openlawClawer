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
    'host': '',
    'password': '',
    'port': 6379, #默认端口
    'database': 0 #默认数据库
}