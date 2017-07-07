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
                #host='118.89.220.36',
                host='172.16.13.165',
                user = 'mha_user',
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
        if item.get('toubao',0) :
            tx.execute("select id from bx_toubao_caiji where url='%s'" % item['url'])
            result = tx.fetchone()
            if result:
                logging.log(logging.INFO, "Already stored in db: %s" % item["url"])
            else:
                tx.execute("SELECT id FROM bx_abc.area WHERE shortname='%s'" % item['city'])
                Area_id = tx.fetchone()
                city_id = Area_id['id'] if Area_id else 100000
                tx.execute("SELECT parentid FROM bx_abc.area WHERE id=%d"%city_id)
                province_id = tx.fetchone()['parentid']
                province_id = province_id if province_id else city_id
                tx.execute("SELECT areaname FROM bx_abc.area WHERE id=%d"%province_id)
                province = tx.fetchone()['areaname']

                try:
                    SQL = """INSERT INTO bx_toubao_caiji(id,name,address,phone,province,province_id,city,city_id,area,area_name,url) 
                                                           VALUES(NULL,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"""
                    SQL = SQL%(item['name'],item["address"],item["phone"],province,province_id,item["city"],city_id,item['area'],item['area_name'],item['url'])
                    #print SQL,'~~~~~~~~~~'
                    tx.execute(SQL)
                except Exception, e:
                    print e, item['url']
                else:
                    logging.log(logging.INFO, "Item stored in db: %s" % item["url"])
                    pass
        else:
            tx.execute("select uid from agent_caiji_sj where url='%s'"%item['url'])
            result = tx.fetchone()
            if result:
                logging.log(logging.INFO,"Already stored in db: %s"%item["url"])
            else:
                tx.execute("SELECT id FROM bx_abc.area WHERE shortname='%s'" % item['city'])
                Area_id = tx.fetchone()
                city_id = Area_id['id'] if Area_id else 100000
                tx.execute("SELECT cid FROM bx_abc.bx_company WHERE comname LIKE '%%%s%%'" % item['company'])
                CID = tx.fetchone()
                if not CID:
                    tx.execute("SELECT cid FROM bx_abc.bx_company WHERE comname LIKE '%%%s%%'"%item['company'][:4])
                    CID = tx.fetchone()
                if u'太平' in item['company'] :
                    CID={'cid':63}
                if u'太平洋' in item['company'] :
                    CID={'cid':99}
                if u'中国人民' in item['company'] or 'PICC' in item['company'] or 'picc' in item['company'] :
                    CID={'cid':56}
                cid = CID['cid'] if CID else 0
                try:
                    SQL = """INSERT INTO agent_caiji_sj(uid,name,phone,company,cid,city,city_id,work_address,url) 
                                                   VALUES(NULL,'%s','%s','%s','%s','%s','%s','%s','%s')"""
                    SQL=SQL%(item['name'],item["phone"],item["company"],cid,item["city"],city_id,item['address'],item['url'])
                    #print SQL,'~~~~~~~~~~'
                    tx.execute(SQL)
                except Exception,e:
                    print e,item['url']
                else:
                    logging.log(logging.INFO,"Item stored in db: %s" % item["url"])
                    pass
    def handle_error(self,e):
        logging.log(logging.ERROR,str(e))
