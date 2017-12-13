#!/usr/bin/env python

# encoding: utf-8

'''

@author: sml2h3

@contact: sml2h3@gmail.com

@software: openlawClawer

@file: celeryconfig.py

@time: 17-12-13 下午4:56

@desc: Celery配置文件

'''

from celery.schedules import crontab
from datetime import timedelta
from kombu import Queue
from kombu import Exchange

result_serializer = 'json'

broker_url = "redis://127.0.0.1"
result_backend = "mongodb://127.0.0.1/celery"
timezone = "Asia/Shanghai"
imports = (
    'Tasks.task1'
)