from __future__ import absolute_import

from app import app
import time as Time
import requests,re,random
from lxml import etree

@app.task
def get(item):
    print("正在获取：%s\n" % item[0])
    # 代理服务器
    print("正在获取代理IP")
    try:
        ip_r = requests.get("http://api.ip.data5u.com/dynamic/get.html?order={order}&sep=0", headers={'Host': 'api.ip.data5u.com'})
    except Exception as e:
        print("当前IP提取服务不可用，休息一秒后重试")
        Time.sleep(1)

        return get(item)
    ip_text = ip_r.text
    ip_array = ip_text.split('\r\n')
    if len(ip_array) < 1:
        print("当前未获取到可用代理IP，等待5秒后重试！")
        Time.sleep(5)
        return get(item)
    index = 0
    ip = ip_array[index]
    print("获取到的为："+ ip + "\r\n")
    proxies = {
        "http": "http://" + ip,
        "https": "http://" + ip
    }
    print(proxies)
    url = "http://openlaw.cn%s" % item[1]
    try:
        init_r = requests.get(url,proxies=proxies)
    except requests.exceptions.ConnectionError as e:
        print("当前代理并发数受到限制，休眠1秒更换")
        Time.sleep(1)
        return get(item)
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
        try:
            result = requests.get(url, cookies=login_r_cookies_new, proxies=proxies, headers=header)
        except requests.exceptions.ConnectionError as e:
            print("当前代理并发数受到限制，休眠1秒更换")
            Time.sleep(1)
            return get(item)
        if result.status_code == 200:
            tree = etree.HTML(result.text)
            # 文书标题
            title_tmp = tree.xpath('//*[@id="ht-kb"]/article/header/h2')
            if len(title_tmp) > 0:
                title = title_tmp[0].text
            else:
                title = '空'
            # 判决日期
            time_tmp = tree.xpath('//*[@id="sidebar"]/section[1]/ul/li[3]')
            if len(time_tmp) > 0:
                time = time_tmp[0].text
            else:
                time = '空'
            # 案号
            no_tmp = tree.xpath('//*[@id="sidebar"]/section[1]/ul/li[1]')
            if len(no_tmp) > 0:
                no = no_tmp[0].text
            else:
                no = '空'
            # 审理法院
            court_tmp = tree.xpath('//*[@id="sidebar"]/section[1]/ul/li[2]')
            if len(court_tmp) > 0:
                court = court_tmp[0].text
            else:
                court = "空"

            # 处理文书主体
            # Litigants
            litigants_tmp = tree.xpath('//*[@id="Litigants"]/p')
            if len(litigants_tmp) > 0:
                litigants = ""
                for item in litigants_tmp:
                    litigants = litigants + item.xpath('string(.)')
            else:
                litigants = "空"
            #explain
            explain_tmp = tree.xpath('//*[@id="Explain"]/p')
            if len(explain_tmp) > 0:
                explain = ""
                for item in explain_tmp:
                    explain = explain + item.xpath('string(.)')
            else:
                explain = "空"
            #procedure
            procedure_tmp = tree.xpath('//*[@id="Procedure"]/p')
            if len(procedure_tmp) > 0:
                procedure = ""
                for item in procedure_tmp:
                    procedure = procedure + item.xpath('string(.)')
            else:
                procedure = "空"

            # facts
            facts_tmp = tree.xpath('//*[@id="Facts"]/p')
            if len(facts_tmp) > 0:
                facts = ""
                for item in facts_tmp:
                    facts = facts + item.xpath('string(.)')
            else:
                facts = "空"

            # opinion
            opinion_tmp = tree.xpath('//*[@id="Opinion"]/p')
            if len(opinion_tmp) > 0:
                opinion = ""
                for item in opinion_tmp:
                    opinion = opinion + item.xpath('string(.)')
            else:
                opinion = "空"
            # verdict
            verdict_tmp = tree.xpath('//*[@id="Verdict"]/p')
            if len(verdict_tmp) > 0:
                verdict = ""
                for item in verdict_tmp:
                    verdict = verdict + item.xpath('string(.)')
            else:
                verdict = "空"
            # inform
            inform_tmp = tree.xpath('//*[@id="Inform"]/p')
            if len(inform_tmp) > 0:
                inform = ""
                for item in inform_tmp:
                    inform = inform + item.xpath('string(.)')
            else:
                inform = "空"
            # ending
            ending_tmp = tree.xpath('//*[@id="Ending"]/p')
            if len(ending_tmp) > 0:
                ending = ""
                for item in ending_tmp:
                    ending = ending + item.xpath('string(.)')
            else:
                ending = "空"
            collection = {
                'title': title,
                'time': time,
                'no': no,
                'court': court,
                'litigants': litigants,
                'explain': explain,
                'procedure': procedure,
                'facts': facts,
                'opinion': opinion,
                'verdict': verdict,
                'inform': inform,
                'ending': ending
            }
            return collection
        else:
            print("网络异常，重新更换代理IP")
            return get(item)
    else:
        print("当前IP不可用，准备重新获取")
        return get(item)

def get_j_token(token):
    return token[2:4] + 'n' + token[0:1] + 'p' + token[4:8] + 'e' + token[1:2] + token[16:len(token)] + token[8:16]