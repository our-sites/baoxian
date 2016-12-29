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
        tx.execute("select uid from bx_vipuser  where certificate_code = '%s' " %(item['certificate_code'] ))
        result = tx.fetchone()
        if result:
            logging.log(logging.DEBUG,"Item already stored in db: %s"  % item["certificate_code"])
        else:
            #print item['chapter_name']
            #pass
            try:
                #print "insert into bx_vipuser('uid','bx_com','introduce','real_name','province','city','evelop_code','certificate_code','info_url') values(NULL ,'%s','%s', '%s','%s','%s','%s', '%s','%s')" %(item['company_name'], item['introduce'], item['name'],item["province_name"], item['city_name'], item['evelop_code'],item["certificate_code"],item['des_url'])
                tx.execute("insert into bx_vipuser(uid,bx_com,introduce,real_name,province,city,evelop_code,certificate_code,info_url) \
                values(NULL ,'%s','%s', '%s','%s','%s','%s', '%s','%s')" %(item['company_name'], item['introduce'], item['name'],item["province_name"], item['city_name'], item['evelop_code'],item["certificate_code"],item['murl']))
            except Exception,e:
                print e,item
            else:
                logging.log(logging.DEBUG,"Item stored in db: %s" % item["name"])
                pass
    def handle_error(self,e):
        logging.log(logging.ERROR,str(e))
