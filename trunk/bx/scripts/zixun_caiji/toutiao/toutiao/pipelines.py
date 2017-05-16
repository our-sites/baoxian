# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
import time
class UserPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool(
                dbapiName='MySQLdb',
                db = 'bx_caiji',
                host='172.16.13.165',
                user = 'root',
                passwd = '123456',
                cursorclass = MySQLdb.cursors.DictCursor,
                charset = 'utf8',
                use_unicode = True,
        )
    #pipeline默认调用
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert,item)
        query.addErrback(self.handle_error)
        return item
    #将每行更新或写入数据库中
    def _conditional_insert(self, tx, item):
        tx.execute("select id from zixun where url='%s'"%item['url'])
        result = tx.fetchone()
        if result:
            logging.log(logging.INFO,"Already stored in db: %s"%item["url"])
        else:
            try:
                SQL = """INSERT INTO zixun(id,type,url,addtime,keywords,content,publishtime,writer,title) VALUES(NULL,%s,'%s',%s,'%s','%s',%s,'%s','%s')"""%(item['type'],item["url"],int(time.time()),item["keyword"],item["content"],item['publishtime'],item['writer'],item['title'])
                tx.execute(SQL)
            except Exception,e:
                print e,item['url']
            else:
                logging.log(logging.INFO,"Item stored in db: %s" % item["url"])
                pass
    def handle_error(self,e):
        logging.log(logging.ERROR,str(e))