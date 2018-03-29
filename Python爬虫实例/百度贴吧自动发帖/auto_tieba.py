# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     auto_tieba
   Description :
   Author :       linhanqiu
   date：          2/2/18
-------------------------------------------------
   Change Activity:
                   2/2/18:
-------------------------------------------------
"""
__author__ = 'linhanqiu'

import aiohttp
import json
import asyncio
import re
class Login:
    def __init__(self):
        try:
            import uvloop
            asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        except ImportError as e:
            pass
        self.loop = asyncio.get_event_loop()
        self.session = aiohttp.ClientSession()
    async def _get_token(self):
        url_token = 'https://passport.baidu.com/v2/api/?getapi&tpl=pp&apiver=v3&class=login'
        headers = {
            'Host':'passport.baidu.com',
            'Cookie':'BAIDUID=4868A5C96AD46FF1A18CC05CCB21613C:FG=1; BIDUPSID=4868A5C96AD46FF1A18CC05CCB21613C; PSTM=1517193281; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; HOSUPPORT=1; PSINO=1; H_PS_PSSID=1432_19033_21118_22160; UBI=fi_PncwhpxZ%7ETaJcw%7ECb%7ETvo8lWMbj3EBc4; FP_UID=98cecf2b16992ca799b432f36191d60d',
        }
        res = await self.session.get(url_token,headers=headers)
        data = await res.text()
        data = json.loads(data.replace('\'', '\"'))
        token = data['data']['token']
        return token
    async def _login(self):
        """登陆百度贴吧，如果登陆成功，保存cookie到json文本，下次登陆可以直接从文本中cookie登陆，无需账号密码
                Args:
                    username (str): 百度账号
                    password (str): 百度账号密码
                """
        url_login = 'https://passport.baidu.com/v2/api/?login'
        data = {
            'username': '17610771895',
            'password': 'linhanqiu',
            'u': 'https://passport.baidu.com/',
            'tpl': 'tb',
            'apiver': 'v3',
            'tt': '1456579434395',
            # 'token': await self._get_token(),
            'token':'5f9d425faefc8219937e712afa26b66e',
            'staticpage': 'https://passport.baidu.com/static/passpc-account/html/v3Jump.html',
            'isPhone': 'false',
            'charset': 'GBK',
            'callback': 'parent.bd__pcbs__n2tlwc'}

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Referer': 'https://passport.baidu.com/v2/?login',
        }
        res = await self.session.post(url_login, data=data, headers=headers)
        print("1",res.cookies)
        res1 = await self.session.get('http://www.baidu.com')
        print("2",res1.cookies)
        res2 = await self.session.get('http://www.baidu.com')
        print("3", res2.cookies)
        # a = re.search(u'个人中心', text)
        # if self._check_login():
        #     with open('cookie.json', 'w') as f:
        #         json.dump(self.session.cookies.get_dict(), f)
        #     print('login...')
        # else:
        #     print('password or username error!')
        # print(res.headers)
        # print(res)
        # return res
    def _close_all(self):
        self.session.close()
        self.loop.close()
    def __call__(self, *args, **kwargs):
        a = self.loop.run_until_complete(self._login())
        print(a)
        self._close_all()

if __name__ == '__main__':
    test = Login()
    test()