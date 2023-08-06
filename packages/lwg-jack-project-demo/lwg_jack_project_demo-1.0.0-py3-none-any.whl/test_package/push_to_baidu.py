import sys
import time

import requests
from bs4 import BeautifulSoup as bp

site_url = 'https://jacksonary.github.io/baidusitemap.xml'
headers = {'User-Agent': 'curl/7.12.1',
           'Host': 'data.zz.baidu.com',
           'Content-Type': 'text/plain',
           'Content-Length': '83'}
push_target = 'http://data.zz.baidu.com/urls?site=https://jacksonary.github.io&token=L6cPsSRw1h9z5sv9'


def get_(data):
    print("begin push data: {}".format(data))
    try:
        r = requests.post(url=push_target, data=data)
        print(r.status_code)
        print(r.content)
        print("data pushed succeed")
        print
    except Exception as exc:
        print("occur error: {}".format(exc))
        print("data pushed failed")
        print


def push(self):
    print('百度自动推送开启....', 'utf-8')

    try:
        print('获取baidusitemap链接....', 'utf-8')
        # 需要安装 lxml pip 依赖
        data_ = bp(requests.get(site_url).content, 'lxml')

        print('---------------------------------')
        if data_ is None:
            print("data is null")
            sys.exit(0)

        urls = []
        for x, y in enumerate(data_.find_all('loc')):
            # urls.append(y.string)
            get_(y.string)
            time.sleep(2)
        # get_(urls)
    except Exception as e:
        print("occur error: {}".format(e))
    print('all have been pushed')
