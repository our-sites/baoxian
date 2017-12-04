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
                db = 'wechat',
                host='113.10.195.169',
                #host='172.16.13.165',
                user = 'dba_user',
                passwd = 'gc895316',
                cursorclass = MySQLdb.cursors.DictCursor,
                charset = 'utf8',
                use_unicode = True
        )
    #pipeline默认调用
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert,item)
        query.addErrback(self.handle_error)
        return item
    #将每行更新或写入数据库中
    def _conditional_insert(self, tx, item):
        if item.get('zixun',0) :
            try:
                SQL = """INSERT INTO wx_fb_news(newid,cateid,title,abstract,show_url,content,state,pubtime,addtime,url) 
                                      VALUES(NULL,%s,'%s','%s','%s','%s',1,%s,%s,'%s')"""
                SQL = SQL%(item['cateid'],item["title"],item["abstract"],item["show_url"],item['content'],item['pubtime'],item['addtime'],item['url'])
                tx.execute(SQL)
            except Exception, e:
                print e, item['url']
            else:
                logging.log(logging.INFO, "Item stored in db: %s" % item["url"])
                pass
        else:
            tx.execute("select newid from wx_fb_news where url='%s'" % item['url'])
            result = tx.fetchone()
            if result:
                logging.log(logging.INFO, "Already stored in db: %s" % item["url"])
            else:
                try:
                    SQL = """INSERT INTO wx_fb_news(newid,cateid,title,abstract,show_url,content,state,pubtime,addtime,url) 
                                          VALUES(NULL,%s,'%s','%s','%s','%s',1,%s,%s,'%s')"""
                    SQL = SQL%(item['cateid'],item["title"],item["abstract"],item["show_url"],item['content'],item['pubtime'],item['addtime'],item['url'])
                    tx.execute(SQL)
                except Exception, e:
                    print e, item['url']
                else:
                    logging.log(logging.INFO, "Item stored in db: %s" % item["url"])
                    pass
    def handle_error(self,e):
        logging.log(logging.ERROR,str(e))
