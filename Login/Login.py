#-*- coding:utf-8 -*-
# @Time    : 2017/7/21 08:56
# @Author  : Sml2h3
# @Site    : www.ydyd.me
# @File    : Login.py
# @Software: PyCharm
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import random
import requests
import json
import base64
import time
from lxml import etree
from Logger.Logger import Logger
Logger = Logger('Login')


class Login(object):
    def __get_random_account(self):
        account = []
        f = open("Login/account.txt", "r").readlines()
        for line in f:
            account.append(line.rstrip('\n'))
        Logger.info("加载账号清单结束，共获取" + str(len(account)) + "个账号")
        index = random.randint(0, len(account)-1)
        acc = account[index]
        if acc:
            acc = str(acc).split('----')
            return {
                'username': acc[0],
                'password': acc[1]
            }
        else:
            return False

    def _run(self):
        #获取Cookies返回,每次获取新cookies均需要通过此接口
        Logger.info("启动openlaw登录脚本，正在加载账号清单")

        account = self.__get_random_account()
        if account == False:
            Logger.warning("未获取到账号清单,即将退出程序")
            exit()
        Logger.info("<<<<<<<<<<<<<<<<<<<<<<<<<<<<随机获取账号>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        Logger.info("用户名:" + account['username'] + "    密码:" + account['password'])
        Logger.info("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        Logger.info("开启登录账号...")
        cookies = self.__login(account)
        return cookies

    def __login(self, account={'username':'', 'password':''}):
        Logger.info("正在抽取验证码链接...")
        page = requests.session()
        result = page.get("http://openlaw.cn/login.jsp?returnTo=%2Fuser%2F")
        if result and result.status_code == 200:
            if '/Kaptcha?v=' in result.text:
                #页面正常，抽取验证码链接
                html = etree.HTML(result.text)
                kaptcha_url = html.xpath('//*[@id="kaptcha"]/@src')
                if len(kaptcha_url) > 0:
                    Logger.info("成功抽取到验证码链接!")
                    kaptcha_url = 'http://openlaw.cn/' + kaptcha_url[0]
                    kresult = page.get(kaptcha_url)
                    if kresult and kresult.status_code == 200:
                        # code = self.__kaptcha(kresult.content)
                        code = 'y78bv'
                        #似乎验证码随便填，为了以防万一。。
                        if code:
                            code = code
                        else:
                            code = 'y78bv'
                        header = {
                            'Host': 'openlaw.cn',
                            'Connection': 'keep-alive',
                            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36',
                            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                            'Referer': 'http://openlaw.cn/login.jsp',
                            'Accept-Encoding': 'gzip, deflate',
                            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
                            'Content-Type': 'application/x-www-form-urlencoded'
                        }
                        data = {
                            'j_username': account['username'],
                            'j_password': account['password'],
                            'j_verificationcode': str(code),
                            '_spring_security_remember_me': 'true'
                        }
                        result = requests.post("http://openlaw.cn/j_spring_security_check", headers=header, data=data, allow_redirects=False)
                        if result and result.status_code == 302:
                            if "login.jsp" in result.headers['location']:
                                #登录失败
                                Logger.warning("登录账号失败，可能是密码错误，请手动检查↓")
                                Logger.info("用户名:" + account['username'] + "密码:" + account['password'])
                                Logger.info("休息5秒后重试")
                                time.sleep(5)
                                self.__login(self.__get_random_account())
                            elif "http://openlaw.cn/;jsessionid" in result.headers['location']:
                                Logger.info("登陆成功，用户名为:" + account['username'])
                                return result.cookies
                        else:
                            Logger.info("网络不畅通，休息10秒再来吧~")
                            page.close()
                            time.sleep(10)
                            self.__login(self.__get_random_account())
                            return
                else:
                    Logger.warning("未获取到验证码链接,休息10秒再来吧~")
                    page.close()
                    time.sleep(10)
                    self.__login(self.__get_random_account())
                    return
            else:
                Logger.warning("登录页面抓取失败,休息10秒再来吧~")
                page.close()
                time.sleep(10)
                self.__login(self.__get_random_account())
                return
        else:
            Logger.warning("登录页面抓取失败,休息10秒再来吧~")
            page.close()
            time.sleep(10)
            self.__login(self.__get_random_account())
            return

    def __kaptcha(self, img_content):
        Logger.info("正在自动识别登录验证码")
        img_base64 = base64.b64encode(img_content)
        header = {
            'Authorization': 'APPCODE ac83c83601fb40e2bf2436598cc75faf',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        data = {
            'convert_to_jpg': '0',
            'img_base64': img_base64,
            'typeId': '35'
        }
        result = requests.post(url="https://ali-checkcode2.showapi.com/checkcode", headers=header, data=data).text
        try:
            result = json.loads(result)
            if result['showapi_res_code'] == 0:
                if result['showapi_res_body']['ret_code'] == 0:
                    code = result['showapi_res_body']['Result']
                    Logger.info('验证码识别成功，结果为' + str(code))
                    return code
                else:
                    Logger.warning('验证码识别失败')
                    return False
            else:
                Logger.warning('Api调用失败，错误信息' + result['showapi_res_error'])
                return False
        except AttributeError:
            Logger.error('验证码识别出现异常')
            return False

if __name__ == '__main__':
    Login()._run()