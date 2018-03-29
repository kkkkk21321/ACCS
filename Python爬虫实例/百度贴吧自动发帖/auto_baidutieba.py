# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     auto_baidutieba
   Description :
   Author :       linhanqiu
   date：          2/1/18
-------------------------------------------------
   Change Activity:
                   2/1/18:
-------------------------------------------------
"""
__author__ = 'linhanqiu'

from bs4 import BeautifulSoup
import requests
import urllib
import json
import re
import datetime
import os


class Post(object):
    """与需要登陆（权限）相关的类，如发帖，签到，
    """

    def __init__(self, username, password):
        self.base_url = 'http://www.baidu.com'
        self.session = requests.Session()
        try:
            self._get_cookies()
        except IOError as e:
            print(e)
        if self._check_login():
            print('from cache...')
        else:
            # 防止cookie过期失效，如果失效则清除cookie
            self.session.cookies.clear()
            self.session.get(self.base_url)
            self.login(username, password)

    def _get_tbs(self):
        url_tbs = 'http://tieba.baidu.com/dc/common/tbs'
        return self.session.get(url_tbs).json()['tbs']

    def _get_token(self):
        url_token = 'https://passport.baidu.com/v2/api/?getapi&tpl=pp&apiver=v3&class=login'
        res = self.session.get(url_token)
        data = json.loads(res.text.replace('\'', '\"'))
        token = data['data']['token']
        return token

    def _get_cookies(self):
        """从文本中获得cookie
        """
        with open('cookie.json') as f:
            try:
                cookies = json.load(f)
            except json.JSONDecodeError as e:
                cookies=''
            if cookies:
                self.session.cookies.update(cookies)

    def _check_login(self):
        """验证是否登陆成功
        Returns:
            Boolean: 是否登陆成功
        """
        res = self.session.get(self.base_url)
        # print(res.content.decode())
        if re.search(u'个人中心', res.text):
            return True
        return False

    def login(self, username, password):
        """登陆百度贴吧，如果登陆成功，保存cookie到json文本，下次登陆可以直接从文本中cookie登陆，无需账号密码
        Args:
            username (str): 百度账号
            password (str): 百度账号密码
        """
        url_login = 'https://passport.baidu.com/v2/api/?login'
        data = {
            'username': username,
            'password': password,
            'u': 'https://passport.baidu.com/',
            'tpl': 'tb',
            'apiver': 'v3',
            'tt': '1456579434395',
            'token': self._get_token(),
            'staticpage': 'https://passport.baidu.com/static/passpc-account/html/v3Jump.html',
            'isPhone': 'false',
            'charset': 'GBK',
            'callback': 'parent.bd__pcbs__n2tlwc'
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Referer': 'https://passport.baidu.com/v2/?login',
        }
        res = self.session.post(
            url_login, data=data, headers=headers)
        print(res.cookies)
        if self._check_login():
            with open('cookie.json', 'w') as f:
                json.dump(self.session.cookies.get_dict(), f)
            print('login...')
        else:
            print('password or username error!')
        # print(res.headers)
        # print(res)
        return res

    def sign(self, kw='太原科技大学'):
        """签到
        Args:
            kw (str, '太原科技大学'): 签到的贴吧
        """
        url_sign = 'http://tieba.baidu.com/sign/add'
        data = {
            'ie': 'utf-8',
            'kw': kw,
            'tbs': self._get_tbs()
        }
        headers = {
            'Host': 'tieba.baidu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'DNT': '1'
        }
        res = self.session.post(url_sign, data=data, headers=headers)
        return res.json()

    def post(self, content, tid, kw='太原科技大学', fid='266662'):
        """百度贴吧回复帖子
        Args:
            content (str): 回复帖子的内容
            tid (str): 回复帖子的ID，http://tieba.baidu.com/p/2674337275，即2674337275
            kw (str, optional): 吧名，即太原科技大学
            fid (str, optional): 吧ID
        Returns:
            TYPE: 百度贴吧的相应json，err_code可查看是否发送成功
        """
        url_post = 'http://tieba.baidu.com/f/commit/post/add'
        tbs = self._get_tbs()
        data = {
            'ie': 'utf-8',
            'kw': kw,
            'fid': fid,
            'tid': tid,
            'content': content,
            'is_login': 1,
            'rich_text': '1',
            'tbs': tbs,
            '__type__': 'reply'
        }
        headers = {
            'Host': 'tieba.baidu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'DNT': '1'
        }
        res = self.session.post(url_post, data=data, headers=headers)
        return res.json()
aa=Post('17610771895','linhanqiu')
#
# import asyncio
# from aiohttp import ClientSession
# url = 'http://httpbin.org/cookies'
# cookies = {'cookies_are': 'working'}
# async def a():
#     async with ClientSession(cookies=cookies) as session:
#         # print(session.__dict__)
#         async with session.get(url) as resp:
#             a = await resp.json()
#             print(resp.headers)
#             return a
# l = asyncio.get_event_loop().run_until_complete(a())
# print(l)
