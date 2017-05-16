# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
import time,sys

reload(sys)
sys.setdefaultencoding('utf-8')

'''
CREATE TABLE `fenxiang` (
  `fid` int(11) NOT NULL AUTO_INCREMENT COMMENT '分享ID',
  `title` varchar(255) NOT NULL COMMENT '分享标题',
  `province` varchar(30) NOT NULL COMMENT '省份',
  `province_id` int(11) DEFAULT NULL COMMENT '省份ID',
  `company` varchar(100) NOT NULL COMMENT '保险公司名称',
  `cid` int(11) DEFAULT NULL COMMENT '保险公司ID',
  `info` text NOT NULL COMMENT '分享内容',
  `url` varchar(150) NOT NULL COMMENT 'Url地址',
  `flag` tinyint(2) NOT NULL DEFAULT '0' COMMENT '标记何种分享,1签单分享,2增员分享,3案例分析',
  `mark` int(11) NOT NULL DEFAULT '0' COMMENT '标记是否已上线,未上线为0,已上线为线上id',
  PRIMARY KEY (`fid`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8 COMMENT='签单、增员分享采集表'
'''

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
        COM = { u'太平洋人寿':99, u'中国人保':56, u'人保健康':57, u'安盛保险':4, u'民生保险':49, u'英大人寿':78, u'阳光人寿':76 }
        tx.execute("select fid from fenxiang where url='%s'"%item['url'])
        result = tx.fetchone()
        tx.execute('SELECT id FROM bx_abc.area WHERE shortname="%s"'%item['province'])
        P = tx.fetchone() 
        tx.execute('SELECT cid FROM bx_abc.bx_company WHERE comname  LIKE "%%%s%%"'%item['company'])
        C = tx.fetchone() 
        if result:
            logging.log(logging.INFO,"Already stored in db: %s"%item["url"])
        else:
            try:
                if P :
                   province_id = P['id']
                else :
                    province_id = 0
                if C :
                   cid = C['cid']
                else :
                    if item['company'] in COM.keys():
                        cid = COM.get(item['company'],0)
                    else :
                        cid = 0
                SQL = "INSERT INTO fenxiang(fid,title,province,province_id,company,cid,info,url,flag) VALUES(NULL,'%s','%s',%s,'%s',%s,'%s','%s',%s)"%(item['title'],item["province"],province_id,item['company'],cid,item['info'],item['url'],item['flag'])
                #print SQL,'~~~~~~~~~~'
                tx.execute(SQL)
            except Exception,e:
                print e,item['url'],'%%%%%%%%%%%%%%%%%%%%%%%%%%%'
            else:
                logging.log(logging.INFO,"Item stored in db: %s" % item["url"])
                pass
    def handle_error(self,e):
        logging.log(logging.ERROR,str(e))
