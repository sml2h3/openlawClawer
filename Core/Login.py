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
from __future__ import absolute_import
import os,requests,re
import execjs
import time,json,random
from Account.account import account
from .Chaoji import Chaoji
from lxml import etree

class Login():

    def __init__(self):
        self.username = ""
        self.password = ""
        self.link = "http://openlaw.cn/Kaptcha.jpg?v=1d795f07406440708f9a2c2af5ede11b"

    def run(self):
        account_num = len(account)
        if account_num > 0:
            index = random.randint(0, account_num - 1)
            acc = account[index]
            self.username = acc[0]
            self.password = acc[1]
            return self.login()
        else:
            print("账号数目过少，请添加openlaw的账号\r\n")
            exit()

    def login(self):
        init_r = requests.get("http://openlaw.cn/login.jsp")
        if init_r.status_code == 200:
            init_r_cookies = init_r.cookies
            init_r_html = init_r.text
            tree = etree.HTML(init_r_html)
            # 取csrf
            print("正在获取csrf_token\r\n")
            _csrf = tree.xpath('//*[@id="login-form"]/input')[0].get('value')
            print("获取csrf_token完成，值为:%s" % _csrf)
            #获取文本型验证码
            print("正在将图片验证码识别为文本验证码\r\n")
            code = self.dis_code(init_r_cookies)
            while code == False:
                print("识别失败，休眠2秒后重新获取图片验证码\r\n")
                time.sleep(2)
                print("正在将图片验证码识别为文本验证码\r\n")
                code = self.dis_code(init_r_cookies)
            print("图片验证码识别成功，结果为%s\r\n" % code)
            print("当前使用的账号为%s,进行密码加密算法破解" % self.username)
            encrypted = self.encrypt()
            print("破解加密算法成功!加密后的密码为\r\n%s\r\n" % encrypted)
            print("正在进行登录请求")
            data = {
                "_csrf": _csrf,
                "username": self.username,
                "password": encrypted,
                "code": code,
                "_spring_security_remember_me": "true"
            }
            login_r = requests.post("http://openlaw.cn/login", data=data, cookies=init_r_cookies, allow_redirects=False)
            if login_r.status_code == 302:
                if 'success' in login_r.headers['Location']:
                    #登陆成功
                    login_r_cookies = login_r.cookies
                    target_r = requests.get("http://openlaw.cn/search/judgement/type?causeId=270cfcd1df47453d9ff4b8d40901a587",cookies=init_r_cookies)
                    v_token =  re.search(r'window.v="(.+?)"', target_r.text).group(1)
                    j_token = self.get_j_token(v_token)
                    j_token = {
                        'j_token': j_token
                    }

                    login_r_cookies_new = requests.utils.add_dict_to_cookiejar(init_r_cookies, j_token)

                    # cookies = requests.utils.dict_from_cookiejar(login_r_cookies_new)
                    return login_r_cookies_new
                else:
                    print("登录失败，休眠5秒后尝试重连\r\n")
                    time.sleep(5)
                    return self.run()

            else:
                print("网络出现异常，等待10秒后重试\r\n")
                return self.login()

        else:
            print("当前网络连接异常，等待十秒后重试。\r\n")
            time.sleep(10)
            return self.login()

    def get_j_token(self, token):
        return token[2:4] + 'n' + token[0:1] + 'p' + token[4:8] + 'e' + token[1:2] + token[16:len(token)] + token[8:16]

    def encrypt(self):
        # 加密密码
        path = os.getcwd()
        path = path + "/Core/encrypt.js"
        content = open(path).read()
        phantom = execjs.get('PhantomJS')
        encrypt = phantom.compile(content)
        encrypted = encrypt.call('keyEncrypt',self.password)
        return encrypted

    def dis_code(self, cookies):
        # 识别验证码
        image = requests.get(self.link, cookies=cookies)
        if image.status_code == 200:
            # filename = str(int(time.time())) + '.jpg'
            # path = os.getcwd()+'/Code/'+filename
            # open(path, 'wb').write(image.content)
            dis = Chaoji()
            dis_result_json = dis.PostPic(image.content,'1005')
            # dis_result_json = json.loads(dis_result)
            if dis_result_json['err_str'] == 'OK':
                return dis_result_json['pic_str']
            else:
                return False
        else:
            return False


if __name__ == '__main__':
    Login('111','WENanzhe123').run()