#-*- coding:utf-8 -*-
# @Time    : 2017/7/20 12:02
# @Author  : Sml2h3
# @Site    : www.ydyd.me
# @File    : test.py
# @Software: PyCharm

if __name__ == '__main__':
    str = "_4848d5597e870c081d228d4b03db35e9"
    cookie = str[2: 4] + 'n' + str[0: 1] + 'p' + str[4: 8] + 'e' + str[1: 2] + str[16: len(str)-1] +str[8: 16]
    print cookie