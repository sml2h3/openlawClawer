#!/usr/bin/env python

# encoding: utf-8

'''

@author: sml2h3

@contact: sml2h3@gmail.com

@software: openlawClawer

@file: Login.py

@time: 17-12-13 下午4:56

@desc: openlaw用户自动登录模块

'''
import os,requests
import execjs

class Login():
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def encrypt(self):
        path = os.getcwd()
        path = path + "/encrypt.js"
        content = open(path).read()
        phantom = execjs.get('PhantomJS')
        encrypt = phantom.compile(content)
        result = encrypt.call('keyEncrypt',self.password)
        print(result)

if __name__ == '__main__':
    Login('111','WENanzhe123').encrypt()