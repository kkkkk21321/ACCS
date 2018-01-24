#!/usr/bin/env python3
#-*-coding:utf-8-*-
# __all__=""
# __datetime__=""
# __purpose__=""

import scrapy

import sys
sys.path.append('/home/linhanqiu/LovePet-RealizeNotion/LPRNCrawler/LPRNCrawler')

from scrapy.contrib.loader import ItemLoader
from scrapy.spider import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from items import CpsecspidersItem
import scrapy
import lxml.html as lh
import sys
import time
import os
from urllib.parse import  urljoin
from scrapy.contrib.spiders import CrawlSpider, Rule
from xml.dom.minidom import parse
import xml.dom.minidom


class leleBBSspider(CrawlSpider):

    # 爬虫名称，非常关键，唯一标示
    name = "lele1"

    # 自定义spider
    custom_settings = {
        'ITEM_PIPELINES': {
            'LPRNCrawler.pipelines.MongoLele_1': 300,
        }
    }
    # 域名限定
    allowed_domains = ["club.lelezone.com"]

    # 爬虫的爬取得起始url
    start_urls = [

        # 天涯论坛热帖榜  可以写多个用，分隔

        "http://club.lelezone.com/g4/f53-1/",

    ]
    baseurl = 'http://club.lelezone.com/'

    def parse(self, response):
        # 选择器
        sel = Selector(response)
        item = CpsecspidersItem()
        # 文章url列表
        article_url = sel.xpath(
            '//dt//p/a/@href').extract()
        # 下一页地址
        next_page_url = sel.xpath("//a[@class='paginate'][last()]/@href").extract()

        for url in article_url:
            # 拼接url
            urll = urljoin(self.baseurl, url)
            # 调用parse_item解析文章内容
            request = scrapy.Request(urll, callback=self.parse_item)
            request.meta['item'] = item
            yield request

        if next_page_url[0]:
            # 调用自身进行迭代
            n = next_page_url[0][-2:-1]
            t = list(next_page_url[0])
            if int(n)>0:
                t[8]=  str(int(n)-1)
                tt = ''.join(t)
                request = scrapy.Request(urljoin(self.baseurl, tt), callback=self.parse)
                yield request

    def parse_item(self, response):
        import time
        time = time.strftime("%Y.%m.%d",time.localtime())
        content = ''
        sel = Selector(response)
        item = response.meta['item']
        l = ItemLoader(item=CpsecspidersItem(), response=response)

        article_url = str(response.url)
        article_name = sel.xpath("//div[@class='art-title']/text()").extract()
        article_content = sel.xpath(
            '//div[@id="articleadbox"]//text()').extract()
        article_author = sel.xpath("//p[@class='fl art-name']/text()").extract()
        article_clik_num = sel.xpath('substring-after(//div[@class="atl-info"]/span[3]/text(),"：")').extract()
        article_reply_num = sel.xpath('substring-after(//div[@class="atl-info"]/span[4]/text(),"：")').extract()
        # 文章内容拼起来
        for i in article_content:
            content = content + i
        # 如果文章名为空的情况
        if not article_name:
            article_name="无名"
        article_name = article_name
        content = content
        article_url = article_url
        article_author = article_author[0]
        click_num = article_clik_num[0]
        reply_num = article_reply_num[0]

        l.add_value('title', article_name)
        l.add_value('content', content)
        l.add_value('url', article_url)
        l.add_value('reply', reply_num)
        l.add_value('click', click_num)
        l.add_value('uname', article_author)
        l.add_value('source', "乐乐地带-新手教学")
        l.add_value('typeid', 0)
        l.add_value('datetime', time)
        l.add_value('EmotionalScore', 0)
        yield l.load_item()

class leleBBS2spider(CrawlSpider):

    # 爬虫名称，非常关键，唯一标示
    name = "lele2"

    # 自定义spider
    custom_settings = {
        'ITEM_PIPELINES': {
            'LPRNCrawler.pipelines.MongoLele_2': 300,
        }
    }
    # 域名限定
    allowed_domains = ["club.lelezone.com"]

    # 爬虫的爬取得起始url
    start_urls = [

        # 天涯论坛热帖榜  可以写多个用，分隔

        "http://club.lelezone.com/g4/f50-1/",

    ]
    baseurl = 'http://club.lelezone.com/'

    def parse(self, response):
        # 选择器
        sel = Selector(response)
        item = CpsecspidersItem()
        # 文章url列表
        article_url = sel.xpath(
            '//dt//p/a/@href').extract()
        # 下一页地址
        next_page_url = sel.xpath("//a[@class='paginate'][last()]/@href").extract()

        for url in article_url:
            # 拼接url
            urll = urljoin(self.baseurl, url)
            # 调用parse_item解析文章内容
            request = scrapy.Request(urll, callback=self.parse_item)
            request.meta['item'] = item
            yield request

        if next_page_url[0]:
            # 调用自身进行迭代
            n = next_page_url[0][-2:-1]
            t = list(next_page_url[0])
            if int(n)>0:
                t[8]=  str(int(n)-1)
                tt = ''.join(t)
                request = scrapy.Request(urljoin(self.baseurl, tt), callback=self.parse)
                yield request

    def parse_item(self, response):
        import time
        time = time.strftime("%Y.%m.%d",time.localtime())
        content = ''
        sel = Selector(response)
        item = response.meta['item']
        l = ItemLoader(item=CpsecspidersItem(), response=response)

        article_url = str(response.url)
        article_name = sel.xpath("//div[@class='art-title']/text()").extract()
        article_content = sel.xpath(
            '//div[@id="articleadbox"]//text()').extract()
        article_author = sel.xpath("//p[@class='fl art-name']/text()").extract()
        article_clik_num = sel.xpath('substring-after(//div[@class="atl-info"]/span[3]/text(),"：")').extract()
        article_reply_num = sel.xpath('substring-after(//div[@class="atl-info"]/span[4]/text(),"：")').extract()
        # 文章内容拼起来
        for i in article_content:
            content = content + i
        # 如果文章名为空的情况
        if not article_name:
            article_name="无名"
        article_name = article_name
        content = content
        article_url = article_url
        article_author = article_author[0]
        click_num = article_clik_num[0]
        reply_num = article_reply_num[0]

        l.add_value('title', article_name)
        l.add_value('content', content)
        l.add_value('url', article_url)
        l.add_value('reply', reply_num)
        l.add_value('click', click_num)
        l.add_value('uname', article_author)
        l.add_value('source', "乐乐地带-宠物医生")
        l.add_value('typeid', 0)
        l.add_value('datetime', time)
        l.add_value('EmotionalScore', 0)
        yield l.load_item()

class leleBBS3spider(CrawlSpider):

    # 爬虫名称，非常关键，唯一标示
    name = "lele3"

    # 自定义spider
    custom_settings = {
        'ITEM_PIPELINES': {
            'LPRNCrawler.pipelines.MongoLele_3': 300,
        }
    }
    # 域名限定
    allowed_domains = ["club.lelezone.com"]

    # 爬虫的爬取得起始url
    start_urls = [

        # 天涯论坛热帖榜  可以写多个用，分隔

        "http://club.lelezone.com/g4/f51-1/",

    ]
    baseurl = 'http://club.lelezone.com/'

    def parse(self, response):
        # 选择器
        sel = Selector(response)
        item = CpsecspidersItem()
        # 文章url列表
        article_url = sel.xpath(
            '//dt//p/a/@href').extract()
        # 下一页地址
        next_page_url = sel.xpath("//a[@class='paginate'][last()]/@href").extract()

        for url in article_url:
            # 拼接url
            urll = urljoin(self.baseurl, url)
            # 调用parse_item解析文章内容
            request = scrapy.Request(urll, callback=self.parse_item)
            request.meta['item'] = item
            yield request

        if next_page_url[0]:
            # 调用自身进行迭代
            n = next_page_url[0][-2:-1]
            t = list(next_page_url[0])
            if int(n)>0:
                t[8]=  str(int(n)-1)
                tt = ''.join(t)
                request = scrapy.Request(urljoin(self.baseurl, tt), callback=self.parse)
                yield request

    def parse_item(self, response):
        import time
        time = time.strftime("%Y.%m.%d",time.localtime())
        content = ''
        sel = Selector(response)
        item = response.meta['item']
        l = ItemLoader(item=CpsecspidersItem(), response=response)

        article_url = str(response.url)
        article_name = sel.xpath("//div[@class='art-title']/text()").extract()
        article_content = sel.xpath(
            '//div[@id="articleadbox"]//text()').extract()
        article_author = sel.xpath("//p[@class='fl art-name']/text()").extract()
        article_clik_num = sel.xpath('substring-after(//div[@class="atl-info"]/span[3]/text(),"：")').extract()
        article_reply_num = sel.xpath('substring-after(//div[@class="atl-info"]/span[4]/text(),"：")').extract()
        # 文章内容拼起来
        for i in article_content:
            content = content + i
        # 如果文章名为空的情况
        if not article_name:
            article_name="无名"
        article_name = article_name
        content = content
        article_url = article_url
        article_author = article_author[0]
        click_num = article_clik_num[0]
        reply_num = article_reply_num[0]

        l.add_value('title', article_name)
        l.add_value('content', content)
        l.add_value('url', article_url)
        l.add_value('reply', reply_num)
        l.add_value('click', click_num)
        l.add_value('uname', article_author)
        l.add_value('source', "乐乐地带-宠物美容")
        l.add_value('typeid', 0)
        l.add_value('datetime', time)
        l.add_value('EmotionalScore', 0)
        yield l.load_item()

class leleBBS4spider(CrawlSpider):

    # 爬虫名称，非常关键，唯一标示
    name = "lele4"

    # 自定义spider
    custom_settings = {
        'ITEM_PIPELINES': {
            'LPRNCrawler.pipelines.MongoLele_4': 300,
        }
    }
    # 域名限定
    allowed_domains = ["club.lelezone.com"]

    # 爬虫的爬取得起始url
    start_urls = [

        # 天涯论坛热帖榜  可以写多个用，分隔

        "http://club.lelezone.com/g4/f52-1/",

    ]
    baseurl = 'http://club.lelezone.com/'

    def parse(self, response):
        # 选择器
        sel = Selector(response)
        item = CpsecspidersItem()
        # 文章url列表
        article_url = sel.xpath(
            '//dt//p/a/@href').extract()
        # 下一页地址
        next_page_url = sel.xpath("//a[@class='paginate'][last()]/@href").extract()

        for url in article_url:
            # 拼接url
            urll = urljoin(self.baseurl, url)
            # 调用parse_item解析文章内容
            request = scrapy.Request(urll, callback=self.parse_item)
            request.meta['item'] = item
            yield request

        if next_page_url[0]:
            # 调用自身进行迭代
            n = next_page_url[0][-2:-1]
            t = list(next_page_url[0])
            if int(n)>0:
                t[8]=  str(int(n)-1)
                tt = ''.join(t)
                request = scrapy.Request(urljoin(self.baseurl, tt), callback=self.parse)
                yield request

    def parse_item(self, response):
        import time
        time = time.strftime("%Y.%m.%d",time.localtime())
        content = ''
        sel = Selector(response)
        item = response.meta['item']
        l = ItemLoader(item=CpsecspidersItem(), response=response)

        article_url = str(response.url)
        article_name = sel.xpath("//div[@class='art-title']/text()").extract()
        article_content = sel.xpath(
            '//div[@id="articleadbox"]//text()').extract()
        article_author = sel.xpath("//p[@class='fl art-name']/text()").extract()
        article_clik_num = sel.xpath('substring-after(//div[@class="atl-info"]/span[3]/text(),"：")').extract()
        article_reply_num = sel.xpath('substring-after(//div[@class="atl-info"]/span[4]/text(),"：")').extract()
        # 文章内容拼起来
        for i in article_content:
            content = content + i
        # 如果文章名为空的情况
        if not article_name:
            article_name="无名"
        article_name = article_name
        content = content
        article_url = article_url
        article_author = article_author[0]
        click_num = article_clik_num[0]
        reply_num = article_reply_num[0]

        l.add_value('title', article_name)
        l.add_value('content', content)
        l.add_value('url', article_url)
        l.add_value('reply', reply_num)
        l.add_value('click', click_num)
        l.add_value('uname', article_author)
        l.add_value('source', "乐乐地带-狗狗训练")
        l.add_value('typeid', 0)
        l.add_value('datetime', time)
        l.add_value('EmotionalScore', 0)
        yield l.load_item()