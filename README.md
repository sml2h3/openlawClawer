# openlawClawer V1.1 使用手册文档
[![Github All Releases](https://img.shields.io/github/downloads/atom/atom/total.svg)](https://github.com/sml2h3/openlawClawer)  [![Read the Docs](https://img.shields.io/readthedocs/pip.svg)](https://github.com/sml2h3/openlawClawer)
## 环境条件
使用环境  | 版本要求
------------- | -------------
Python  | >= 3
PhantomJs  | >= 2.0
Redis  |  >= 3
MongoDB  | >= 2.6

## 开始安装

> 安装手册以Ubuntu16.04系统为标准，其他系统不保证稳定性，您也可以通过提交Pull Request添加您所使用系统的本产品安装手册作为补充！

 1. 安装Python3以及PhantomJs环境

``` shell
sudo apt-get install python3.5
```
PhantomJs只需要主端安装
``` shell
sudo apt-get install phantomjs
```

 2. 安装PIP包依赖


``` shell
pip3 install -r requirements.txt
```
 3. 获得程序



``` shell
git clone https://github.com/sml2h3/openlawClawer.git
```

## 配置程序

 ### 配置Celery
 打开Config目录，找到celeryconfig.py文件
 #### BROKER
 broker_url 为redis
 redis_url格式为

> redis://:password@hostname:port/db_number

``` python
broker_url = "redis://127.0.0.1"
```
#### RESULT_BACKEND
result_backend为mongodb
mongodb_url格式为

> mongodb://userid:password@hostname:port/database_name

``` python
result_backend = "mongodb://127.0.0.1/celery"
```
#### 代理IP提取
经过在开发中使用各家的产品结合openlaw网站爬取的特殊性，经过慎重考虑将采用[无忧代理][1]的爬虫代理IP产品（非广告），当然也可使用作者github中的[代理池工具][2]做提取。
打开Tasks目录中的get_content文件，修改第13行get_ip变量，将{order}替换成你的订单号。（如果您不是使用无忧代理，还需额外修改第15行Host的值）


  ## 运行使用


 - 主端直接运行


``` shell
python3 openlawClawer.py
```

 - 子端在项目根目录运行



``` shell
celery worker -A app -l info -concurrency=5
```

> 其中concurrency参数制定子节点并发数，默认5即可，过大可能会引发一些突发问题（如代理IP提取频率受限等，量力而行），如果使用本地代理池进行提取代理IP，可以考虑增大。最好不要超过10

## 捐赠支持

> 本项目无偿给大家使用，但没一个版本的维护都需要作者的精力才得以维持。如果本项目为您或者贵公司带来了很多方便，可以通过Star或捐赠的方式支持作者继续维护本项目。毕竟Openlaw网站最近更新的有点频繁，哈哈。感谢各位支持！捐赠后我会定期将捐赠者（捐赠大于30元）的名单发布在本README，您可以在备注中额外添加您的公司主页或者个人主页，将统一展示在下方。
![enter description here][3]![enter description here][4]

> 本项目是经过测试后才提交，故如有技术问题可提交ISSUE或者考虑收费服务。如您需要有偿服务解决问题，可微信或支付宝扫码并在转账留言留下您的联系方式并标注需要解决问题，我会在下班后与您进行联系。

|   捐赠名单  |  主页   |
| --- | --- |
|   李佳璐  |  -   |
|   北京敬一科技有限公司  |   -  |

  [1]: http://www.data5u.com/
  [2]: https://github.com/sml2h3/proxypool
  [3]: http://i4.bvimg.com/623795/46aeff9232e66019.png
  [4]: http://i4.bvimg.com/623795/c13701483f7aa837.jpg