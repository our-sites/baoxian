# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import logging
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors

class UserPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool(
                dbapiName='MySQLdb',
                db = 'bx_abc',
                host='172.16.13.177',
                user = 'root',
                passwd = '123456',
                cursorclass = MySQLdb.cursors.DictCursor,
                charset = 'utf8',
                use_unicode = True,
                # host='113.10.195.169',
                # user='dba_user',
                # passwd='gc895316'
        )
    #pipeline默认调用
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert,item)
        query.addErrback(self.handle_error)
        return item
    #将每行更新或写入数据库中
    def _conditional_insert(self, tx, item):
        #print "select zid from bx_consult where title = '%s' and type=%s"  %(item['title'],item['type'] )
        tx.execute("select uid from bx_vipuser_360baoxian  where info_url = '%s' " %(item['info_url'] ))
        result = tx.fetchone()
        if result:
            logging.log(logging.INFO,"Item already stored in db: %s"  % item["info_url"])
        else:
            print item['company_name']
            try:
                tx.execute("insert into bx_vipuser_360baoxian(uid,bx_com,sex ,age,xueli,city,info_url,phone,email,evelop_code,tel,real_name) \
                values(NULL ,'%s','%s','%s','%s','%s', '%s','%s', '%s','%s','%s','%s')" %(item['company_name'], item['sex'],item['age'],item["xueli"], \
                                                                     item['city'],item['info_url'],\
                                                                     item['phone'],item["email"],item["evelop_code"],item["tel"],item["name"]))
            except Exception,e:
                print e
                print "eeeeeeeeeerrrrrrrrrrrrrrrooooooooooooooorrrrrrrrrrr"
            else:
                logging.log(logging.INFO,"Item stored in db: %s" % item["info_url"])
                pass
    def handle_error(self,e):
        logging.log(logging.ERROR,str(e))