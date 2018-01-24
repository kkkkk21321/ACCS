#!/usr/bin/env python3
#-*-coding:utf-8-*-
# __all__=""
# __datetime__=""
# __purpose__="单一的requests请求"

import requests


url = "http://i.baidu.com/"

headers = {
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'accept-encoding': "gzip, deflate, sdch, br",
    'accept-language': "zh-CN,zh;q=0.8,en;q=0.6",
    'cache-control': "no-cache",
    'connection': "keep-alive",
    'host': "i.baidu.com",
    'referer':'https://www.baidu.com/',
    'pragma': "no-cache",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    'x-forwarded-for': "111.202.141.60",
    'postman-token': "df69dfed-82f0-12a7-4873-2695e9323c17"
    }
response = requests.request("GET", url, headers=headers)

print(response.content.decode())