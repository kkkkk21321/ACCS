# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo

class MongoPipeline(object):

    collection_name = ''

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'tianya')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(dict(item))
        return item

class MongoTianya_1(MongoPipeline):
    collection_name = 'yangchongxinqing'

class MongoTianya_2(MongoPipeline):
    collection_name = 'feichangchongwu'

class MongoTianya_3(MongoPipeline):
    collection_name = 'chongmixuetang'

class MongoTianya_4(MongoPipeline):
    collection_name = 'chongwuxinxi'

class MongoTianya_5(MongoPipeline):
    collection_name = 'liuyankanban'

class Mongo1Pipeline(object):

    collection_name = ''

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'cpn')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(dict(item))
        return item

class MongoCpn_1(Mongo1Pipeline):
    collection_name = 'nuoyafangzhou'
class MongoCpn_2(Mongo1Pipeline):
    collection_name = 'gouhualianpian'
class MongoCpn_3(Mongo1Pipeline):
    collection_name = 'maomaoxiyu'
class MongoCpn_4(Mongo1Pipeline):
    collection_name = 'lengxuejiazu'
class MongoCpn_5(Mongo1Pipeline):
    collection_name = 'bainiaoyuan'

class Mongo2Pipeline(object):

    collection_name = ''

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'lele')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(dict(item))
        return item

class MongoLele_1(Mongo2Pipeline):
    collection_name = 'xinshouijaoxue'
class MongoLele_2(Mongo2Pipeline):
    collection_name = 'chongwuyisheng'
class MongoLele_3(Mongo2Pipeline):
    collection_name = 'chongwumeiong'
class MongoLele_4(Mongo2Pipeline):
    collection_name = 'gougouxunlian'

class Mongo3Pipeline(object):

    collection_name = ''

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'baidu')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(dict(item))
        return item
class Mongobaidu_1(Mongo3Pipeline):
    collection_name = 'chongwuba'