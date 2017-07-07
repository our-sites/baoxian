#coding=utf-8
import MySQLdb,MySQLdb.cursors
import time
import jieba
from jieba import analyse
import solr
import random
from ask_ans_reform import get_proxy_cid,get_ansList1,get_ansList2
"""处理提问中答案过少的问题，增加提问的回答数"""
mysql_conf = {
        'host': '118.89.220.36',
        #'host': '172.16.13.165',
        'user': 'mha_user',
        'passwd': 'gc895316',
        'db': 'bx_caiji',
        'charset': 'utf8',
        'init_command': 'set autocommit=0',
        'cursorclass':MySQLdb.cursors.DictCursor
        }

Mysql_conf = {
        #'host': '118.89.220.36',
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

#获取重复的记录
#SQL = "select ansid from bx_answer a where (a.askid,a.ans_content,a.cid,a.city_id) in (select askid,ans_content,cid,city_id from bx_answer group by askid,ans_content,cid,city_id having count(*) > 1) and ansid not in (select max(ansid) from bx_answer group by askid,ans_content,cid,city_id having count(*)>1)"
def main() :
    askid,askid_list=0,[]
    tfidf = analyse.extract_tags
    ask_solr = solr.SolrConnection('http://172.16.13.165:8983/solr/bx_ask')
    ans_solr = solr.SolrConnection('http://172.16.13.165:8983/solr/bx_ask_ans')
    while askid < 41293 :
        SQL="SELECT askid,count(*) AS num FROM bx_answer WHERE askid > %d group by askid order by askid LIMIT 500"%askid

        my_cur.execute(SQL)
        Data = my_cur.fetchall()
        for D in Data :
            if D['num'] <= 2 :
                askid_list.append(int(D['askid']))
                askid=D['askid']
                '''
                my_cur.execute("SELECT askid,ask_content FROM bx_ask WHERE askid=%d"%askid)
                ASK = my_cur.fetchone()
                try :
                    anslist = get_ansList2(ASK, ans_solr, ask_solr, tfidf)
                except :
                    print D
                    continue

                SQL = "INSERT INTO bx_caiji.bx_answer (askid,ans_content,company,cid,province_id,city_id) VALUES"
                # 将获取到的答案与原问题id对应关系生成SQL语句
                for ans in anslist:
                    My_cur.execute("SELECT id FROM bx_abc.area WHERE shortname='%s'" % ans['city'])
                    City_id = My_cur.fetchone()
                    city_id = City_id['id'] if City_id else 100000
                    My_cur.execute("SELECT id FROM bx_abc.area WHERE shortname='%s'" % ans['province'])
                    Province_id = My_cur.fetchone()
                    province_id = Province_id['id'] if Province_id else 100000
                    CID = get_proxy_cid(my_cur, ans['company'], tfidf)
                    if CID :
                        sql = SQL + "(%d,'%s','%s',%d,%d,%d)" % (askid, ans['ans_content'].replace("'", '"'), ans['company'].replace("'", '"'), CID['cid'],province_id, city_id)
                        try:
                            my_cur.execute(sql)
                        except Exception, e:
                            print e
                            continue
                    else:
                        print D,'~~~~~~~~~~~~~'
                        continue
                my_cxn.commit()'''
        else :
            askid+=500
    print len(askid_list)
    SQL = "DELETE FROM bx_ask WHERE askid in "+str(tuple(askid_list))
    print SQL
    #my_cur.execute(SQL)
    my_cxn.commit()

if __name__ == '__main__':
    main()

