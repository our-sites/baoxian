#!/usr/bin/env python
# coding=utf-8
import MySQLdb.cursors
import MySQLdb as mdb
from circinfo import data_handle

import sys
reload(sys)
sys.setdefaultencoding('utf8')

conn= MySQLdb.connect(
        host='172.16.13.177',
        port = 3306,
        user='root',
        passwd='123456',
        db ='bx_abc',cursorclass = MySQLdb.cursors.DictCursor,charset="utf8")
cur = conn.cursor()
#cur.execute("SELECT bx_com,real_name,province,city,phone,evelop_code,certificate_code FROM bx_vipuservobal WHERE length(evelop_code) > 19 order by uid desc")
#allData = cur.fetchall()


my_conn= MySQLdb.connect(
        host='172.16.13.165',
        port = 3306,
        user='root',
        passwd='123456',
        db ='bx_caiji',charset="utf8",cursorclass=MySQLdb.cursors.DictCursor)
my_cur = my_conn.cursor()
my_cur.execute("SELECT uid  FROM bx_vipuser WHERE uid < 35000 AND auth_mark=1 ORDER BY uid DESC LIMIT 1")
UID = my_cur.fetchone()
my_cur.execute("SELECT uid,bx_com,real_name,province,city,phone,evelop_code,certificate_code,introduce FROM bx_vipuser WHERE uid >=17500 AND uid< 35000 AND auth_mark < 1 AND length(evelop_code) > 19 order by uid desc")
allData = my_cur.fetchall()
#print len(allData)
for Data in allData:
    my_cur.execute("SELECT aid FROM agent_auth WHERE evelop_code='%s'"%Data['evelop_code'])
    A = my_cur.fetchall()
    #如果已经被采集过,则跳过这一条数据
    if A :
        print Data['evelop_code']
        continue
    #从http://iir.circ.gov.cn/web/网站拉取验证后的信息
    DATA =data_handle(Data['evelop_code'])
    #对获取到的信息进行甄别后入库
    if len(DATA) > 1 :
        my_cur.execute("SELECT id FROM bx_abc.area WHERE shortname='%s'"%Data['city'])
        City_id=my_cur.fetchone()
        city_id = City_id['id'] if City_id else 100000
        my_cur.execute("SELECT id FROM bx_abc.area WHERE shortname='%s'"%Data['province'])
        Province_id=my_cur.fetchone()
        province_id = Province_id['id'] if Province_id else 100000
        my_cur.execute("SELECT id FROM bx_abc.area WHERE areaname='%s'"%DATA.get(u'执业区域',u'全国'))
        Area_id=my_cur.fetchone()
        area_id = Area_id['id'] if Area_id else 100000
        SQL = "INSERT INTO agent_auth (real_name,sex,phone,evelop_code,evelop_stat,certificate_code,certificate_stat,term_validity,scope_business,practice_area,area_id,company,proxy_cid,province,province_id,city,city_id,bx_com) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');"
        real_name = DATA[u'姓名'] if DATA.get(u'姓名','') else Data['real_name']
        sex = 2 if DATA[u'性别'] == u'女' else 1
        phone = Data.get('phone','').strip()
        evelop_code = Data.get('evelop_code',DATA.get(u'执业证编号',''))
        evelop_stat = 1 if DATA.get(u'执业证状态','') == u'有效' else 2
        evelop_stat = 0 if DATA.get(u'执业证状态','') == u'无' else evelop_stat
        certificate_code = DATA.get(u'资格证书号码') if DATA.get(u'资格证书号码','') else Data.get('certificate_code','').strip()
        certificate_stat = 1 if DATA.get(u'资格证书状态','') == u'有效' else 2
        certificate_stat = 0 if DATA.get(u'资格证书状态','') == u'无' else certificate_stat
        term_validity = DATA.get(u'有效截止日期','')
        scope_business = DATA.get(u'业务范围','')
        practice_area = DATA.get(u'执业区域','')
        company = DATA.get(u'所属公司','')
        bx_com = Data.get('bx_com','')
        SQL = SQL %(real_name,sex,phone,evelop_code,evelop_stat,certificate_code,certificate_stat,term_validity,scope_business,practice_area,area_id,company,0,Data['province'],province_id,Data['city'],city_id,bx_com)
        try :
            my_cur.execute(SQL)
        except :
            print SQL
        else :
            my_cur.execute("UPDATE bx_vipuser SET auth_mark=1 WHERE uid=%s"%Data['uid'])
    else :
        my_cur.execute("UPDATE bx_vipuser SET auth_mark='-1' WHERE uid=%s"%Data['uid'])
        continue
    my_conn.commit()
