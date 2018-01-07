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
from .Login import Login
import requests
import time
from lxml import etree
from Tasks.get_content import get

class Core():

    def __init__(self, causeId, account):
        self.causeId = causeId
        self.page = 1
        self.targetUrl = "http://openlaw.cn/search/judgement/type?causeId=%s" % self.causeId

    def run(self):
        print("启动登录一个账号\r\n")
        user_cookies = Login().login()
        print(user_cookies)
        print("登录成功，准备获取文书列表\r\n")
        list_temp = self.get_list(user_cookies)

        if list_temp == 10001:
            #需要重新登录
            print("系统检测到当前用户已经失效，即将重新登录\r\n")
            return self.run()
        else:
            while len(list_temp) > 0:
                # 抓取了数据
                list_num = len(list_temp)
                print("抓取成功,第%s页共抓取到数据量为:%s" % (self.page, list_num))
                self.send_task(list_temp)
                self.page = self.page + 1
                list_temp = []
                list_temp = self.get_list(user_cookies)
                if list_temp == 10001:
                    # 需要重新登录
                    print("系统检测到当前用户已经失效，即将重新登录\r\n")
                    return self.run()
                    break
            # 没有数据了
            print("所有数据已经抓取完毕，准备退出")
            time.sleep(1)
            exit()

    def send_task(self, task_list):
        for item in task_list:
            get.delay(item)

    def get_list(self, cookies):
        print("正在抓取第%s页数据\r\n" % self.page)
        page_r = requests.get(self.targetUrl + "&page=%s" % self.page, cookies=cookies)
        if page_r.status_code == 200:
            if 'window.v=' in page_r.text:
                return 10001
            if '抱歉' in page_r.text:
                return 10001
            tree = etree.HTML(page_r.text)
            init_list = tree.xpath('//*[@id="ht-kb"]/article/h3/a')
            list_array = []
            for item in init_list:
                item_link = item.get('href')
                item_text = item.text
                item_array = [item_text,item_link]
                list_array.append(item_array)
            return list_array
        else:
            print("网络连接异常，5秒后进行重连\r\n")
            time.sleep(5)
            return self.get_list()
