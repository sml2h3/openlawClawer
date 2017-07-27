#-*- coding:utf-8 -*-
# @Time    : 2017/7/21 17:46
# @Author  : Sml2h3
# @Site    : www.ydyd.me
# @File    : Clawer.py
# @Software: PyCharm
import sys
sys.setrecursionlimit(110000)
import requests
import time
from Logger.Logger import Logger
from gevent import monkey
from Login.Login import Login
monkey.patch_socket()
from lxml import etree
import gevent
from gevent.pool import Pool
# import pymysql
from Config.DB import *
Logger = Logger('Clawer')


class Clawer(object):
    def __init__(self, config, cookies):
        self.conn = config.conn
        self.cookies = cookies
        self.page = 1
        self.ckvalid = True

    def _run_master(self):
        if self.check_j_token():
            gevent.spawn(self.clawer_master).join()
        else:
            self._run_master()

    def _run_slaver(self):
        if self.check_j_token():
            pool = Pool(2)
            while True:
                urls = [ self.conn.spop("urls") for i in range(5) ]
                result = pool.map(self.clawer_slaver, urls)

        else:
            self._run_slaver()

    def check_j_token(self):
        # 判断是否第一次访问
        Logger.info("正在判断是否需要生成j_token")
        result = requests.get("http://openlaw.cn/search/judgement/type?causeId=a3ea79cf193f4e07a27a900e29585dbb&page=1",
                              cookies=self.cookies)
        if result and result.status_code == 200:
            if 'wch3116@hotmail.com' in result.text:
                # 需要
                Logger.info("需要生成j_token，即将开始进入j_token计算")
                v = self.txt_wrap_by('window.v="', '"', result.text)
                j_token = self.__get_j_token(v)
                self.cookies = requests.utils.add_dict_to_cookiejar(self.cookies, {"j_token": j_token})
            else:
                # 不需要
                Logger.info("不需要生成j_token")
            return True
        else:
            Logger.warning("判断失败，休息一会重新判断~")
            time.sleep(5)
        return False

    def clawer_slaver(self, url):
        header = {
            'Host': 'openlaw.cn',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Referer': url,
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        }
        result = requests.get(url, cookies=self.cookies, headers=header)
        if result and result.status_code == 200:

            html = etree.HTML(result.text)
            #判决时间
            time_tem = html.xpath('//*[@id="ht-kb"]/article/header/ul/li[1]/text()')
            if len(time_tem) > 0:
                time = time_tem[0].rstrip().replace(" ", '')
            else:
                time = "0"
            #判决标题
            title_tem = html.xpath('//*[@id="ht-kb"]/article/header/h2/text()')
            if len(title_tem) > 0:
                title = title_tem[0]
            else:
                title = ""
            if title == "":
                self.clawer_slaver(url)
                return
            Logger.info(title)
            #判决法院
            fy_tem = html.xpath('//*[@id="ht-kb"]/article/header/ul/li[2]/a/text()')
            if len(fy_tem) > 0:
                fy = fy_tem[0]
            else:
                fy = ""
            #案号
            ah_tem = html.xpath('//*[@id="ht-kb"]/article/header/ul/li[3]/text()')
            if len(ah_tem) > 0:
                ah = ah_tem[0]
            else:
                ah = ""
            #控告人和控诉人
            content = html.xpath('//*[@id="Litigants"]/p//text()')
            c = ""
            for t in content:
                c += t
            litigants = c
            content = html.xpath('//*[@id="Explain"]/p//text()')
            c = ""
            for t in content:
                c += t
            explain = c
            #诉讼程序
            content = html.xpath('//*[@id="Procedure"]/p//text()')
            c = ""
            for t in content:
                c += t
            procedure = c
            #观点
            content = html.xpath('//*[@id="Opinion"]/p//text()')
            c = ""
            for t in content:
                c += t
            option = c
            #裁定
            content = html.xpath('//*[@id="Verdict"]/p//text()')
            c = ""
            for t in content:
                c += t
            verdict = c
            #通知
            content = html.xpath('//*[@id="Inform"]/p//text()')
            c = ""
            for t in content:
                c += t
            info = c
            #结束语
            content = html.xpath('//*[@id="Ending"]/p//text()')
            c = ""
            for t in content:
                c += t
            end = c
            Logger.info(title)
            # conn = pymysql.connect(host='rm-2ze7441de5149074.redis.rds.aliyuncs.com', port=3306, user='root', passwd='CSDNb405', db='openlaw', charset='utf8')
            # cursor = conn.cursor()
            # result = cursor.execute('insert into law(title, litigants, explain, procedure, opinion, verdict, inform, ending, time, fy, an) vaules(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(str(title), str(litigants), str(explain), str(procedure), str(option), str(verdict), str(info), str(end), str(time), str(fy), str(ah)))
            # conn.commit()
            # cursor.close()
            # conn.close()
            session = DBSession()
            # 创建新User对象:
            new_user = Law(title=title, litigants=litigants, explain=explain, procedure=procedure, opinion=option, verdict=verdict, inform=info, ending=end, time=time, fy=fy, an=ah)
            # 添加到session:
            session.add(new_user)
            # 提交即保存到数据库:
            session.commit()
            session.close()
            # 关闭session:
            Logger.info("任务:"+ url + "完成")

    def clawer_master(self, url=""):
        if url == "":
            page = self.page
            self.page += 1
            url = "http://openlaw.cn/search/judgement/type?causeId=a3ea79cf193f4e07a27a900e29585dbb&page="
            url += str(page)
            # 代理服务器
            proxyHost = "proxy.abuyun.com"
            proxyPort = "9020"

            # 代理隧道验证信息
            proxyUser = "H4871716T867Q1LD"
            proxyPass = "CCAE03DE2E35FBA2"

            proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
                "host": proxyHost,
                "port": proxyPort,
                "user": proxyUser,
                "pass": proxyPass,
            }

            proxy_handler = {
                "http": proxyMeta,
                "https": proxyMeta,
            }

            header = {
                'Host': 'openlaw.cn',
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36',
                'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                'Referer': url,
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            }
            Logger.info("正在抓取的页数为" + str(page))
        result = requests.get(url, cookies=self.cookies, headers=header, proxies=proxy_handler)
        if result and result.status_code == 200:
            if "抱歉不能为您显示更多的内容!" in result.text:
                Logger.info("Cookies已经失效需要重新登录")
                self.cookies = Login()._run()
            html = etree.HTML(result.text)
            href = html.xpath('//*[@id="ht-kb"]/article/h3/a/@href')
            #//*[@id="ht-kb"]/article[2]/h3/a
            if len(href)>0:
                urls = [ 'http://openlaw.cn'+i for i in href ]
                Logger.info("第" + str(page) + "页成功爬取到文书链接，数据量为" + str(len(urls)) + "条")
                Logger.info("正在将任务上传至Redis服务器，等待从机进行下一步操作")
                for url in urls:
                    self.conn.sadd('urls', url)
                Logger.info("上传至Redis服务器成功，即将开始爬去第二页的内容")
            else:
                Logger.info("本页未爬取到链接")
            self.clawer_master()

        else:
            Logger.warning("访问出错，休息一会吧~")
            time.sleep(3)
            self.clawer_master(url)

    def txt_wrap_by(self, start_str, end, html):
        start = html.find(start_str)
        if start >= 0:
            start += len(start_str)
            end = html.find(end, start)
            if end >= 0:
                return html[start:end].strip()

    def __get_j_token(self, str):
        cookie = str[2: 4] + 'n' + str[0: 1] + 'p' + str[4: 8] + 'e' + str[1: 2] + str[16: len(str) - 1] + str[8: 16]
        return cookie
