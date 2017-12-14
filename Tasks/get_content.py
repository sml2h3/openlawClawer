from __future__ import absolute_import

from app import app

import requests,re,random

@app.task
def get(item):
    print("正在获取：%s\n" % item[0])
    # 代理服务器
    print("正在获取代理IP")
    ip_r = requests.get("http://api.xdaili.cn/xdaili-api//privateProxy/applyStaticProxy?spiderId=45b1e7fced9d46d2a0e6609830f17cb5&returnType=1&count=1")
    ip_text = ip_r.text
    ip_array = ip_text.split('\r\n')
    index = random.randint(0,len(ip_array) - 2)
    ip = ip_array[index]
    print("获取到的为："+ ip + "\r\n")
    proxies = {
        "http": "http://" + ip,
        "https": "http://" + ip
    }
    url = "http://openlaw.cn%s" % item[1]
    init_r = requests.get(url,proxies=proxies)
    init_r_cookies = init_r.cookies
    if "window.v=" in init_r.text:
        v_token = re.search(r'window.v="(.+?)"', init_r.text).group(1)
        j_token = get_j_token(v_token)
        j_token = {
            'j_token': j_token
        }
        login_r_cookies_new = requests.utils.add_dict_to_cookiejar(init_r_cookies, j_token)
        header = {
            "Referer": url
        }
        result = requests.get(url, cookies=login_r_cookies_new, proxies=proxies, headers=header)
        print(result.text)
    else:
        print("当前IP不可用，准备重新获取")
        return get(item)

def get_j_token(token):
    return token[2:4] + 'n' + token[0:1] + 'p' + token[4:8] + 'e' + token[1:2] + token[16:len(token)] + token[8:16]

if __name__ == '__main__':
    item = ['111','/judgement/6aad8a2f524841a5b0245cad2e13cee4']
    get(item)
    # ip_r = requests.get(
    #     "http://api.xdaili.cn/xdaili-api//privateProxy/applyStaticProxy?spiderId=45b1e7fced9d46d2a0e6609830f17cb5&returnType=1&count=1")
    # ip_text = ip_r.text
    # ip_array = ip_text.split('\r\n')
    # print(ip_array)
    # proxies = {
    #     "http": "http://183.148.75.196:45834",
    #     "https": "http://183.148.75.196:45834"
    # }
    # result = requests.get("https://www.ipip.net/", proxies=proxies)
    # print(result.text)