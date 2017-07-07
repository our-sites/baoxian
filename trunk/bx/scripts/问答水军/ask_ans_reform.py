#coding=utf-8
#! /usr/bin/env python
#coding=utf-8
__author__ = 'Administrator'
#this is SVN_CODE
#create by 2017/05/25 0023
"""重组问答内容,并将线下的采集内容转移至线上采集库"""

import MySQLdb,MySQLdb.cursors
import time
import jieba
from jieba import analyse
import solr
import random

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

conf = {
            'host': '172.16.13.177',
            'user': 'root',
            'passwd': '123456',
            'db': 'bx_abctest',
            'charset': 'utf8',
            'init_command': 'set autocommit=0',
            'cursorclass':MySQLdb.cursors.DictCursor
            }

def get_proxy_cid(my_cur,company,tfidf):
    if u'人保寿险' in company:
        company= u'中国人保寿险'
    if u'太平人寿' in company:
        company= u'中国太平'
    if u'阳光人寿' in company:
        company= u'阳光保险'
    my_cur.execute('SELECT cid FROM bx_abc.bx_company WHERE shortname="%s"'%company)
    Data = my_cur.fetchone()
    if Data :
        return Data
    else :
        my_cur.execute('SELECT cid FROM bx_abc.bx_company WHERE comname LIKE "%%%s%%"' % company)
        Data = my_cur.fetchone()
        if Data :
            return Data
        else :
            my_cur.execute('SELECT cid FROM bx_abc.bx_company WHERE comname LIKE "%%%s%%"'% ''.join(tfidf(company)))
            Data = my_cur.fetchone()
            if Data :
                return Data
            else :
                if u'人寿' in company:
                    company = company[:-2]
                my_cur.execute(
                    'SELECT cid FROM bx_abc.bx_company WHERE comname LIKE "%%%s%%"' % ''.join(tfidf(company)))
                Data = my_cur.fetchone()
                return Data

def clean_ansList(D,Result):
    R,n = [],0
    for _R in Result:
        # 如果获取的新答案依旧是本提问的原始答案则丢弃、答案重复也丢弃、答案过短也丢弃
        '''
        if int(_R['askid']) == int(D['askid']) or _R in R or len(_R['ans_content']) < 5:
            continue
        else:
            R.append(_R)
        '''
        if _R in R or len(_R['ans_content']) < 5 :
            continue
        if int(_R['askid']) == int(D['askid']) and n < 2:
            n=n+1
            R = [_R] + R
        elif int(_R['askid']) == int(D['askid']) and n >= 2 :
            continue
        else:
            R.append(_R)
    L = len(R)
    #当该提问的答案多于5个的时候防止答案过多,从现有的答案中随机抽取一部分答案
    if L > 5:
        #R = R[L-random.randint(4, L):]
        R=R[:random.randint(5,8)]
    return R

def get_ansList1(D,ans_solr,ask_solr,tfidf):
    askid=0
    ###本方法使用问题A去所有问题中检索类似A的问题B，然后使用问题B的答案回答A问题###
    try :
        result = ask_solr.query('ask_content:"%s"'%D['ask_content'],rows=15)
        if not result:
            return  []
        for r in result:
            if int(r['askid']) == int(D["askid"]) :
                continue
            else :
                askid=r.get('askid',0)
                if askid :
                    #print askid,'~~~~~~~~~~~~~~~~~~~~~~~OK~~~~~~~~~~~'
                    break
        if not askid :
            return []
        Result = ans_solr.query("askid:%d"%askid, rows=5)
    except Exception,e:
        print e,'-------------get_ansList',D['ask_content'],askid,'\r\n\r\n'
        return []
    else :
        #将获取的新答案进行清洗后返回
        return clean_ansList(D,Result)

def get_ansList2(D,ans_solr,ask_solr,tfidf):
    ###本方法使用问题A(提取其关键词)去所有答案中检索，然后使用检索到的答案回答A问题;问题A的所有原答案优先级放到最低###
    try :
        result = ans_solr.query('ans_content:"%s"'%D['ask_content'], rows=15)
    except Exception,e:
        print e,'~~~~~~~~~get_ansList0'
        return []
    else :
        # 将获取的新答案进行清洗后返回
        return clean_ansList(D,result)

def get_ansList3(D,ans_solr,ask_solr,tfidf):
    R=[]
    ###本方法使用问题A的答案A0去所有答案中检索，然后使用检索到的答案回答A问题;问题A的所有原答案优先级放到最低###
    try:
        result = ans_solr.query("askid:%d" % D['askid'], rows=10)
        if not result:
            return []
        for r in result:
            #if len(r['ans_content']) > 60 :
            #    r['ans_content'] = ''.join(tfidf(r['ans_content']))
            Result = ans_solr.query('ans_content:"%s"'%r['ans_content'], rows=5)
            for result in Result:
                R.append(result)
            #print Result,type(Result)
            #R=Result+R
            #if Result :
            #    break
    except Exception, e:
        print e,'##########get_ansList1'
        return clean_ansList(D, R)
    else:
        # 将获取的新答案进行清洗后返回
        return clean_ansList(D, R)

def main():
    cxn = MySQLdb.connect(**conf)
    cur = cxn.cursor()
    my_cxn = MySQLdb.connect(**mysql_conf)
    my_cur = my_cxn.cursor()
    cur.execute('SELECT askid,ask_content FROM bx_ask_188_caiji WHERE usedtime=0 order by askid limit 20000')
    Data = cur.fetchall()
    Time=int(time.time())
    tfidf = analyse.extract_tags
    ask_solr = solr.SolrConnection('http://172.16.13.165:8983/solr/bx_ask')
    ans_solr = solr.SolrConnection('http://172.16.13.165:8983/solr/bx_ask_ans')

    for D in Data:
        ###这里可以选择不同的答案重组方式进行组合###
        #if len(D['ask_content']) > 50 :
        #    D['ask_content']=''.join(tfidf( D['ask_content']))
        anslist=get_ansList3(D,ans_solr,ask_solr,tfidf)
        #如果该提问找不到与之对应的答案则跳过该提问(如果答案与采集的一模一样也跳过)
        if not anslist or len(anslist) < 3 :
            cur.execute('UPDATE bx_ask_188_caiji SET usedtime=1 WHERE askid=%d'%D['askid'])
            continue
        try :
            my_cur.execute('INSERT INTO bx_caiji.bx_ask(ask_content) VALUES ("%s")' % D['ask_content'])
        except :
            cur.execute('UPDATE bx_ask_188_caiji SET usedtime=2 WHERE askid=%d'%D['askid'])
            continue
        else :
            askid = int(my_cur.lastrowid)
        SQL="INSERT INTO bx_caiji.bx_answer (askid,ans_content,company,cid,province_id,city_id) VALUES"
        #将获取到的答案与原问题id对应关系生成SQL语句
        for ans in anslist:
            my_cur.execute("SELECT id FROM bx_abc.area WHERE shortname='%s'" % ans['city'])
            City_id = my_cur.fetchone()
            city_id = City_id['id'] if City_id else 100000
            my_cur.execute("SELECT id FROM bx_abc.area WHERE shortname='%s'" % ans['province'])
            Province_id = my_cur.fetchone()
            province_id = Province_id['id'] if Province_id else 100000
            CID=get_proxy_cid(my_cur,ans['company'],tfidf)
            if CID :
                sql = SQL + "(%d,'%s','%s',%d,%d,%d)" % (askid, ans['ans_content'].replace("'", '"'), ans['company'].replace("'", '"'), CID['cid'], province_id,city_id)
                try :
                    my_cur.execute(sql)
                except Exception,e:
                    print e
                    continue
            else :
                continue

        #将获取到的新对应关系推送到线上的采集库,如果获取到的值为空,则删除已插入的提问
        if len(sql) > 100 :
            #my_cur.execute(SQL[:-1])
            #标记处理到哪里,以防程序中断从头处理造成数据重复
            cur.execute('UPDATE bx_ask_188_caiji SET usedtime=%d WHERE askid=%d'%(Time,D['askid']))
        else :
            my_cur.execute('DELETE FROM bx_caiji.bx_ask WHERE askid=%d'%askid)
        cxn.commit()
        my_cxn.commit()
    my_cxn.close()

if __name__ == '__main__':
    main()
