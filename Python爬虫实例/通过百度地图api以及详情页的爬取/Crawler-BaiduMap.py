#!/usr/bin/env python3
#-*-coding:utf-8-*-
# __all__=""
# __datetime__=""
# __purpose__=""

import aiohttp
import ujson
import asyncio
from functools import reduce
import re
from lxml import etree
import csv


class CrawlerBaiduMap:
    def __init__(self):
        try:
            import uvloop
            asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        except ImportError as e:
            print("导入uvloop错误")
        self.loop = asyncio.get_event_loop()
        self.headers = {
            'User-Agent': '',
        },
        self.ua_set = [
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
            "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        ]
        # poi查询 url
        self.poi_url = 'http://api.map.baidu.com/place/v2/search'

        # poi查询 params
        self.params = {
            'q': '烤鱼店',
            'tag':'美食',
            'region': '北京',
            'scope': '2',
            'page_size': '20',
            # 'filter': 'industry_type:cater|sort_name:distance|sort_rule:1|groupon:1',
            'page_num': 20,
            'output': 'json',
            # 百度地图令牌
            'ak': 'YZzXIf6mjrTVtj8YMAxnIHfEs7bfHmEl',
        }
        # uid url
        self.uid_url = 'http://map.baidu.com/detail?qt=ugccmtlist&from=mapwap&type=cater&orderBy=1&pageCount=10&uid=name&pageIndex=code'

        # detail_url
        self.detail_url = 'http://api.map.baidu.com/place/detail?uid=name&output=html&source=placeapi_v2'
        # total
        self.pagenum = 30
        # detail_num
        self.detail_num = 100
        # poi_info
        self.data = []

        # uid
        self.uid = []
        # uid_info
        self.uid_info = []

        # url_info
        self.url_info = []

    async def poi_req(self, i):
        """
        poi查询接口
        :return:
        """
        async with aiohttp.ClientSession() as sess:
            self.params['page_num'] = i
            async with sess.get(self.poi_url, params=self.params) as r:
                fr = await r.text()
                fr = ujson.loads(fr)['results']
                return fr

    async def bound_poi_req(self, sem,i):
        """
        poi查询接口增加限制版
        :return:
        """
        async with sem:
            return await self.poi_req(i)

    async def url_req(self, uid):
        """
        调用url详情页 获取店铺标签
        :param uid:
        :return: tags 标签集
        """
        async with aiohttp.ClientSession() as sess:
            detail_url = re.sub(r'name', uid, self.detail_url)
            async with sess.get(detail_url) as r:
                fr = await r.text()
                result = etree.HTML(fr)
                tags = result.xpath('//span[@class="label "]//text()')
                return tags

    async def uid_req(self, uid, page):
        """
        调用uid详情页
        :param uid:page
        :return:
        """
        uid_set = []
        async with aiohttp.ClientSession() as sess:
            uid_url = re.sub(r'name', uid, self.uid_url)
            for i in range(1, page):
                asyncio.sleep(1)
                uid_url = re.sub(r'code', str(i), uid_url)
                async with sess.get(uid_url) as r:
                    fr = await r.text()
                    fr = ujson.loads(fr)
                    if fr.get('comment'):
                        fr = fr['comment']['comment_list']
                        fr = [(i['cn_name'], i['content']) for i in fr]
                        uid_set.append(fr)
                    else:
                        break
        return uid_set

    def into_csv(self):
        """
        写入csv文件
        :return:
        """
        out = open("baidustore_test2.csv", "a", newline="")
        csv_writer = csv.writer(out, dialect="excel")
        csv_writer.writerow(("店铺名称","地址","人均价格","是否有团购","电话号码","店铺标签","评论信息"))
        for index, v in enumerate(self.data):
            row = []
            row.append(v['name'])# 第一列
            row.append(v['address'])# 第二列
            row.append(v['detail_info'].get('price', ' '))# 第三列
            row.append(v['detail_info'].get('groupon_num', '没有团购')) # 第四列
            row.append(v.get('telephone',' ')) # 第五列
            row.append(self.url_info[index]) # 第六列
            row.append(self.uid_info[index]) # 第七列
            csv_writer.writerow(row)

    async def flow(self):
        """
        爬取流程
        :return:
        """
        # 任务组
        sem = asyncio.Semaphore(100)
        tasks = [
            asyncio.ensure_future(
                self.bound_poi_req(sem,i)) for i in range(
                20, int(
                    self.pagenum))]
        r = await asyncio.gather(*tasks)
        # 获得所有店铺信息
        self.data = reduce(lambda x, y: x + y, r)
        # 获得店铺uid的集合
        self.uid = [i['uid'] for i in self.data]
        tasks_tags = [
            asyncio.ensure_future(
                self.url_req(uid)) for uid in self.uid]
        r_tags = await asyncio.gather(*tasks_tags)
        self.url_info = [i for i in r_tags]
        tasks_details = [
            asyncio.ensure_future(
                self.uid_req(
                    uid,
                    self.detail_num)) for uid in self.uid]
        r_details = await asyncio.gather(*tasks_details)
        self.uid_info = [i for i in r_details]

    def __call__(self, *args, **kwargs):
        self.loop.run_until_complete(self.flow())
        self.into_csv()


if __name__ == "__main__":
    # 实例
    test = CrawlerBaiduMap()
    test()
