# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.exceptions import DropItem
from pymongo import MongoClient
import pymysql

class MongoPipeline(object):
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls,crawler):
         return cls(
             mongo_uri=crawler.settings.get('MONGO_URI'),
             mongo_db=crawler.settings.get('MONGO_DB')
         )
    def open_spider(self,spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self,item,spider):
        self.db[item.collection].update({'description':item['description']},{'$set':dict(item)},True)
        return item

    def close_spider(self,spider):
        self.client.close()

class MysqlPipeline(object):
    def __init__(self,host,user,password,port,database):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.database = database

    @classmethod
    def from_crawler(cls,crawler):
        return cls (
            host = crawler.settings.get('HOST'),
            port = crawler.settings.get('PORT'),
            user = crawler.settings.get('USER'),
            password = crawler.settings.get('PASSWORD'),
            database = crawler.settings.get('DATABASE')
        )

    def open_spider(self,spider):
        self.db = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                                  database=self.database, charset='utf8')
        self.cur = self.db.cursor()

    def process_item(self,item,spider):
        data = dict(item)
        keys = ','.join(data.keys())
        values = ','.join(['%s']*len(data.values()))
        # sql = 'INSERT INTO %s (%s) values (%s)' % (item.table,keys,values)
        sql = 'INSERT IGNORE INTO {table}({keys})VALUES ({values})'.format(table=item.table,keys=keys,values=values)
        self.cur.execute(sql,tuple(data.values()))
        self.db.commit()
        return item

    def close_spider(self, spider):
        self.db.close()
