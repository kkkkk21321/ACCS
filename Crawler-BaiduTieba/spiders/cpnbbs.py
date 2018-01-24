#!/usr/bin/env python3
#-*-coding:utf-8-*-
# __all__=""
# __datetime__=""
# __purpose__="cpn宠物论坛爬取"

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


class CpnBBSspider(CrawlSpider):

    # 爬虫名称，非常关键，唯一标示
    name = "cpn1"

    # 自定义spider
    custom_settings = {
        'ITEM_PIPELINES': {
            'LPRNCrawler.pipelines.MongoCpn_1': 300,
        }
    }
    # 域名限定
    allowed_domains = ["chinapet.net"]

    # 爬虫的爬取得起始url
    start_urls = [

        # cpn论坛热帖榜  可以写多个用，分隔

        "http://www.chinapet.net/bbs/forum-85.html",

    ]
    baseurl = 'http://www.chinapet.net/bbs/'

    def parse(self, response):
        # 选择器
        sel = Selector(response)
        item = CpsecspidersItem()
        # 文章url列表
        article_url = sel.xpath(
            '//span[@class="topictitle"]/a/@href').extract()
        # 下一页地址
        next_page_url = sel.xpath("//span[@class='nav']/a[3]/@href").extract()
        for url in article_url:
            # 拼接url
            urll = urljoin(self.baseurl, url)
            # 调用parse_item解析文章内容
            request = scrapy.Request(urll, callback=self.parse_item)
            request.meta['item'] = item
            yield request

        if next_page_url[0]:
            # 调用自身进行迭代
            print(urljoin(self.baseurl, next_page_url[0]))
            request = scrapy.Request(urljoin(self.baseurl, next_page_url[0]), callback=self.parse)
            yield request

    def parse_item(self, response):
        import time
        time = time.strftime("%Y.%m.%d",time.localtime())
        content = ''
        sel = Selector(response)
        item = response.meta['item']
        l = ItemLoader(item=CpsecspidersItem(), response=response)

        article_url = str(response.url)
        article_name = sel.xpath('//a[@class="maintitle"]/text()').extract()
        article_content = sel.xpath(
            '//span[@class="postbody"]/text()').extract()
        article_author = sel.xpath("//td[@class='row1'][1]/span[@class='postdetails']/text()[1]").extract()
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
        l.add_value('source', "cpn论坛-诺亚方舟")
        l.add_value('typeid', 0)
        l.add_value('datetime', time)
        l.add_value('EmotionalScore', 0)
        yield l.load_item()

class CpnBBS2spider(CrawlSpider):

    # 爬虫名称，非常关键，唯一标示
    name = "cpn2"

    # 自定义spider
    custom_settings = {
        'ITEM_PIPELINES': {
            'LPRNCrawler.pipelines.MongoCpn_2': 300,
        }
    }
    # 域名限定
    allowed_domains = ["chinapet.net"]

    # 爬虫的爬取得起始url
    start_urls = [

        # cpn论坛热帖榜  可以写多个用，分隔

        "http://www.chinapet.net/bbs/forum-8.html",

    ]
    baseurl = 'http://www.chinapet.net/bbs/'

    def parse(self, response):
        # 选择器
        sel = Selector(response)
        item = CpsecspidersItem()
        # 文章url列表
        article_url = sel.xpath(
            '//span[@class="topictitle"]/a/@href').extract()
        # 下一页地址
        next_page_url = sel.xpath('//td[@nowrap="nowrap"]/span[@class="nav"]/a[1]/@href').extract()
        for url in article_url:
            # 拼接url
            urll = urljoin(self.baseurl, url)
            # 调用parse_item解析文章内容
            request = scrapy.Request(urll, callback=self.parse_item)
            request.meta['item'] = item
            yield request

        if next_page_url[0]:
            # 调用自身进行迭代
            request = scrapy.Request(urljoin(self.baseurl, next_page_url[0]), callback=self.parse)
            yield request

    def parse_item(self, response):
        import time
        time = time.strftime("%Y.%m.%d",time.localtime())
        content = ''
        sel = Selector(response)
        item = response.meta['item']
        l = ItemLoader(item=CpsecspidersItem(), response=response)

        article_url = str(response.url)
        article_name = sel.xpath('//a[@class="maintitle"]/text()').extract()
        article_content = sel.xpath(
            '//table[@class="attachtable"]//text()').extract()
        article_author = sel.xpath("//td[@class='row1'][1]/span[@class='postdetails']/text()[1]").extract()
        article_clik_num = sel.xpath('substring-after(//div[@class="atl-info"]/span[3]/text(),"：")').extract()
        article_reply_num = sel.xpath('substring-after(//div[@class="atl-info"]/span[4]/text(),"：")').extract()
        # print(article_name)
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
        l.add_value('source', "cpn论坛-狗话连篇")
        l.add_value('typeid', 0)
        l.add_value('datetime', time)
        l.add_value('EmotionalScore', 0)
        yield l.load_item()

class CpnBBS3spider(CrawlSpider):

    # 爬虫名称，非常关键，唯一标示
    name = "cpn3"

    # 自定义spider
    custom_settings = {
        'ITEM_PIPELINES': {
            'LPRNCrawler.pipelines.MongoCpn_3': 300,
        }
    }
    # 域名限定
    allowed_domains = ["chinapet.net"]

    # 爬虫的爬取得起始url
    start_urls = [

        # cpn论坛热帖榜  可以写多个用，分隔

        "http://www.chinapet.net/bbs/forum-20.html",

    ]
    baseurl = 'http://www.chinapet.net/bbs/'

    def parse(self, response):
        # 选择器
        sel = Selector(response)
        item = CpsecspidersItem()
        # 文章url列表
        article_url = sel.xpath(
            '//span[@class="topictitle"]/a/@href').extract()
        # 下一页地址
        next_page_url = sel.xpath('//td[@nowrap="nowrap"]/span[@class="nav"]/a[1]/@href').extract()
        for url in article_url:
            # 拼接url
            urll = urljoin(self.baseurl, url)
            # 调用parse_item解析文章内容
            request = scrapy.Request(urll, callback=self.parse_item)
            request.meta['item'] = item
            yield request

        if next_page_url[0]:
            # 调用自身进行迭代
            request = scrapy.Request(urljoin(self.baseurl, next_page_url[0]), callback=self.parse)
            yield request

    def parse_item(self, response):
        import time
        time = time.strftime("%Y.%m.%d",time.localtime())
        content = ''
        sel = Selector(response)
        item = response.meta['item']
        l = ItemLoader(item=CpsecspidersItem(), response=response)

        article_url = str(response.url)
        article_name = sel.xpath('//a[@class="maintitle"]/text()').extract()
        article_content = sel.xpath(
            '//table[@class="attachtable"]//text()').extract()
        article_author = sel.xpath("//td[@class='row1'][1]/span[@class='postdetails']/text()[1]").extract()
        article_clik_num = sel.xpath('substring-after(//div[@class="atl-info"]/span[3]/text(),"：")').extract()
        article_reply_num = sel.xpath('substring-after(//div[@class="atl-info"]/span[4]/text(),"：")').extract()
        # print(article_name)
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
        l.add_value('source', "cpn论坛-猫猫细语")
        l.add_value('typeid', 0)
        l.add_value('datetime', time)
        l.add_value('EmotionalScore', 0)
        yield l.load_item()

class CpnBBS4spider(CrawlSpider):

    # 爬虫名称，非常关键，唯一标示
    name = "cpn4"

    # 自定义spider
    custom_settings = {
        'ITEM_PIPELINES': {
            'LPRNCrawler.pipelines.MongoCpn_4': 300,
        }
    }
    # 域名限定
    allowed_domains = ["chinapet.net"]

    # 爬虫的爬取得起始url
    start_urls = [

        # cpn论坛热帖榜  可以写多个用，分隔

        "http://www.chinapet.net/bbs/forum-121.html",

    ]
    baseurl = 'http://www.chinapet.net/bbs/'

    def parse(self, response):
        # 选择器
        sel = Selector(response)
        item = CpsecspidersItem()
        # 文章url列表
        article_url = sel.xpath(
            '//span[@class="topictitle"]/a/@href').extract()
        # 下一页地址
        next_page_url = sel.xpath('//td[@nowrap="nowrap"]/span[@class="nav"]/a[1]/@href').extract()
        for url in article_url:
            # 拼接url
            urll = urljoin(self.baseurl, url)
            # 调用parse_item解析文章内容
            request = scrapy.Request(urll, callback=self.parse_item)
            request.meta['item'] = item
            yield request

        if next_page_url[0]:
            # 调用自身进行迭代
            request = scrapy.Request(urljoin(self.baseurl, next_page_url[0]), callback=self.parse)
            yield request

    def parse_item(self, response):
        import time
        time = time.strftime("%Y.%m.%d",time.localtime())
        content = ''
        sel = Selector(response)
        item = response.meta['item']
        l = ItemLoader(item=CpsecspidersItem(), response=response)

        article_url = str(response.url)
        article_name = sel.xpath('//a[@class="maintitle"]/text()').extract()
        article_content = sel.xpath(
            '//table[@class="attachtable"]//text()').extract()
        article_author = sel.xpath("//td[@class='row1'][1]/span[@class='postdetails']/text()[1]").extract()
        article_clik_num = sel.xpath('substring-after(//div[@class="atl-info"]/span[3]/text(),"：")').extract()
        article_reply_num = sel.xpath('substring-after(//div[@class="atl-info"]/span[4]/text(),"：")').extract()
        # print(article_name)
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
        l.add_value('source', "cpn论坛-冷血家族")
        l.add_value('typeid', 0)
        l.add_value('datetime', time)
        l.add_value('EmotionalScore', 0)
        yield l.load_item()


class CpnBBS5spider(CrawlSpider):

    # 爬虫名称，非常关键，唯一标示
    name = "cpn5"

    # 自定义spider
    custom_settings = {
        'ITEM_PIPELINES': {
            'LPRNCrawler.pipelines.MongoCpn_5': 300,
        }
    }
    # 域名限定
    allowed_domains = ["chinapet.net"]

    # 爬虫的爬取得起始url
    start_urls = [

        # cpn论坛热帖榜  可以写多个用，分隔

        "http://www.chinapet.net/bbs/forum-84.html",

    ]
    baseurl = 'http://www.chinapet.net/bbs/'

    def parse(self, response):
        # 选择器
        sel = Selector(response)
        item = CpsecspidersItem()
        # 文章url列表
        article_url = sel.xpath(
            '//span[@class="topictitle"]/a/@href').extract()
        # 下一页地址
        next_page_url = sel.xpath('//td[@nowrap="nowrap"]/span[@class="nav"]/a[1]/@href').extract()
        for url in article_url:
            # 拼接url
            urll = urljoin(self.baseurl, url)
            # 调用parse_item解析文章内容
            request = scrapy.Request(urll, callback=self.parse_item)
            request.meta['item'] = item
            yield request

        if next_page_url[0]:
            # 调用自身进行迭代
            request = scrapy.Request(urljoin(self.baseurl, next_page_url[0]), callback=self.parse)
            yield request

    def parse_item(self, response):
        import time
        time = time.strftime("%Y.%m.%d",time.localtime())
        content = ''
        sel = Selector(response)
        item = response.meta['item']
        l = ItemLoader(item=CpsecspidersItem(), response=response)

        article_url = str(response.url)
        article_name = sel.xpath('//a[@class="maintitle"]/text()').extract()
        article_content = sel.xpath(
            '//table[@class="attachtable"]//text()').extract()
        article_author = sel.xpath("//td[@class='row1'][1]/span[@class='postdetails']/text()[1]").extract()
        article_clik_num = sel.xpath('substring-after(//div[@class="atl-info"]/span[3]/text(),"：")').extract()
        article_reply_num = sel.xpath('substring-after(//div[@class="atl-info"]/span[4]/text(),"：")').extract()
        # print(article_name)
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
        l.add_value('source', "cpn论坛-百鸟园")
        l.add_value('typeid', 0)
        l.add_value('datetime', time)
        l.add_value('EmotionalScore', 0)
        yield l.load_item()