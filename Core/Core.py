#!/usr/bin/env python

# encoding: utf-8

'''

@author: sml2h3

@contact: sml2h3@gmail.com

@software: openlawClawer

@file: Core.py

@time: 17-12-13 下午5:12

@desc: 运行内核

'''
class Core():

    def __init__(self, causeId, account):
        self.causeId = causeId
        self.account = account

    def run(self):
        self.targetUrl = "http://openlaw.cn/search/judgement/type?causeId=%s" % self.causeId
        accountNum = len(self.account)

