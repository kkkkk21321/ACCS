#!/usr/bin/env python3
#-*-coding:utf-8-*-
# __all__=""
# __datetime__=""
# __purpose__=""

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
# 导入获取项目配置的模块
from scrapy.utils.project import get_project_settings
# 导入蜘蛛模块(即自己创建的spider)
from spiders.baidutieba import (Baiduspider)

configure_logging()
# get_project_settings() 必须得有，不然"HTTP status code is not handled or not allowed"
runner = CrawlerRunner(get_project_settings())
runner.crawl(Baiduspider)

d = runner.join()
d.addBoth(lambda _: reactor.stop())
reactor.run() # the script will block here until all crawling jobs are finished