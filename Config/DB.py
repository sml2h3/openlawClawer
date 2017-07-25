#-*- coding:utf-8 -*-
# @Time    : 2017/7/25 05:05
# @Author  : Sml2h3
# @Site    : www.ydyd.me
# @File    : DB.py
# @Software: PyCharm
from sqlalchemy import Column, create_engine
from sqlalchemy.types import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

# 定义User对象:
class Law(Base):
    # 表的名字:
    __tablename__ = 'law'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    litigants = Column(Text)
    explain = Column(Text)
    procedure = Column(Text)
    opinion = Column(Text)
    verdict = Column(Text)
    inform = Column(Text)
    ending = Column(Text)
    time = Column(VARCHAR(14))
    fy = Column(VARCHAR(50))
    an = Column(VARCHAR(255))

# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:CSDNb405@r-2ze7441de5149074.redis.rds.aliyuncs.com/openlaw?charset=utf8')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

if __name__ == '__main__':
    # 创建session对象:
    session = DBSession()
    # 创建新User对象:
    new_user = Law(litigants='111', explain='222', time="2012")
    # 添加到session:
    session.add(new_user)
    # 提交即保存到数据库:
    session.commit()
    # 关闭session:
    session.close()