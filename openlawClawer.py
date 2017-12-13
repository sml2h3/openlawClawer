#!/usr/bin/env python

# encoding: utf-8

'''

@author: sml2h3

@contact: sml2h3@gmail.com

@software: openlawClawer

@file: openlawClawer.py

@time: 17-12-13 下午4:55

@desc: 爬虫主程序

'''
from Account.account import account
from Core.Core import Core


if __name__ == '__main__':
    print("欢迎使用openlaw爬虫系统!\r\n")
    print("当前版本号:v1.1\r\n")
    causeId = ""
    while causeId == "":
        causeId = input("请输入需要爬去的casueId。(如不清楚如何获得causeId,请参考本项目主页:https://github.org)\r\n")
    print("当前输入的causeId为%s" % causeId)
    if len(account) == 0:
        print("账号数目为0，请参照项目主页文档添加openlaw账号")
        exit(0)
    core = Core(causeId=causeId, account=account)
    core.run()