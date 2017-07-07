#coding=utf-8
import MySQLdb,MySQLdb.cursors
import time

"""增加水军的提问者"""
mysql_conf = {
        'host': '118.89.220.36',
        'user': 'mha_user',
        'passwd': 'gc895316',
        'db': 'bx_caiji',
        'charset': 'utf8',
        'init_command': 'set autocommit=0',
        'cursorclass':MySQLdb.cursors.DictCursor
        }

Mysql_conf = {
        'host': '172.16.13.165',
        'user': 'mha_user',
        'passwd': 'gc895316',
        'db': 'bx_caiji',
        'charset': 'utf8',
        'init_command': 'set autocommit=0',
        'cursorclass':MySQLdb.cursors.DictCursor
        }

my_cxn = MySQLdb.connect(**mysql_conf)
my_cur = my_cxn.cursor()

My_cxn = MySQLdb.connect(**Mysql_conf)
My_cur = My_cxn.cursor()

my_cur.execute('SELECT phone,sex,birthday,province_id,city_id FROM bx_abc.bx_user WHERE uid > 1999 AND usertype=2')
data = my_cur.fetchall()
SQL = "INSERT INTO bx_abc.bx_user(uid,username,salt,state,phone,sex,birthday,usertype,addtime,password,province_id,city_id) VALUES(%d,'%s','dfce3a',1,'%s','%s','%s',1,%d,'d08c9c2976347ec5fdfae8fd15268a17','%s','%s')"
for n in xrange(1788,1962):
    d=data[n-1788]
    sql = SQL %(n,d['phone']+n,d['phone']+n,d['sex'],d['birthday'],int(time.time()),int(d['province_id']),int(d['city_id']))
    print sql
    #my_cur.execute(sql)
#my_cxn.commit()

'''
###修正问题的提问者信息###
my_cur.execute('SELECT uid FROM bx_abc.bx_user WHERE uid<1999 AND usertype=1 ORDER BY phone')
data = my_cur.fetchall()
my_cur.execute('SELECT askid FROM bx_abc.bx_ask WHERE askid<1002 and askid>985')
Data = my_cur.fetchall()
for D in Data :
        index=D['askid']%214
        my_cur.execute('update bx_abc.bx_ask set uid=%d WHERE askid=%d'%(data[index]['uid'],D['askid']))
my_cxn.commit()
'''
