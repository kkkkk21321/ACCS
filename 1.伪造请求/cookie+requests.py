#!/usr/bin/env python3
#-*-coding:utf-8-*-
# __all__=""
# __datetime__=""
# __purpose__="添加cookie请求"


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
    'cookie':'BAIDUID=66901EB81E3B49685808906E46C843C4:FG=1; BIDUPSID=66901EB81E3B49685808906E46C843C4; PSTM=1506342962; __cfduid=d2b2d29406bbe9cc42c24094eee4d3a5f1509334518; Hm_lvt_4010fd5075fcfe46a16ec4cb65e02f04=1516700903,1516802417,1516802431; H_PS_PSSID=1427_21103_20930; BDRCVFR[Fc9oatPmwxn]=G01CoNuskzfuh-zuyuEXAPCpy49QhP8; PSINO=1; FP_UID=940a1496225159ada86d8bbf9dc1f86e; BDUSS=FVGOUVzakFrblNZZH5NSEVIWVNjU2ZWTlZSZ0R6SkNtaFFpaU13aXJBcU9ybzlhQVFBQUFBJCQAAAAAAAAAAAEAAAA3VXuxu6rPxNPQxMzGpAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAI4haFqOIWhaU; PHPSESSID=h67otjgo8o1qauvbnil6bcjqh0; Hm_lpvt_4010fd5075fcfe46a16ec4cb65e02f04=1516802431',
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    'x-forwarded-for': "111.202.141.60",
    'postman-token': "df69dfed-82f0-12a7-4873-2695e9323c17"
    }
response = requests.request("GET", url, headers=headers)

print(response.content.decode())