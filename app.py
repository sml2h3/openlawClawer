#!/usr/bin/env python

# encoding: utf-8

'''

@author: sml2h3

@contact: sml2h3@gmail.com

@software: openlawClawer

@file: app.py

@time: 17-12-13 下午4:55

@desc: 实例化Celery

'''
from celery import Celery
# 实例化一个Celery
app = Celery("demo")
# 读取配置文件并批量配置
app.config_from_object("Config.celeryconfig")

if __name__ == '__main__':

    app.start()