#! /usr/bin/env python
#coding=utf-8
__author__ = 'Administrator'
#this is SVN_CODE
#create by 2017/05/25 0023

"""水军伪装用户提问"""

import MySQLdb,MySQLdb.cursors
import time
import random
import requests
import json

mysql_conf = {
            'host': '127.0.0.1',#118.89.220.36
            #'host': '118.89.220.36',
            #'host': '172.16.13.165',
            'user': 'mha_user',
            'passwd': 'gc895316',
            'db': 'bx_abc',
            'charset': 'utf8',
            'init_command': 'set autocommit=0',
            'cursorclass':MySQLdb.cursors.DictCursor
            }

def post_ask(url,Data,Time):
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
        ]
    user_agent = user_agent_list[Time % 8]
    headers = {'user-agent':user_agent, 'Referer':"https://www.bao361.cn/ask/"}
    try :
        DATA = requests.post(url, headers=headers, data=Data)
    except Exception,e :
        print e
        return  {"status":False,"message":str(e)}
    else :
        return DATA
def get_ask_user(my_cur,y,Time):
    uidlist=''
    my_cur.execute('SELECT uid FROM bx_caiji.bx_ask WHERE uid>0 AND online_time>%d'%(Time - 86400*3))
    Userdata = my_cur.fetchall()
    for U in Userdata:
        if U['uid'] :
            uidlist=uidlist+str(U['uid'])+','

    ###如果以上都没有合适的人选，那就传个默认的###
    if uidlist :
        my_cur.execute('SELECT uid FROM bx_abc.bx_user WHERE uid<1999 AND uid>1 AND usertype=1 AND state=1 AND uid NOT IN (%s) LIMIT %d'%(uidlist[:-1],(y*6)))
    else :
        my_cur.execute('SELECT uid FROM bx_abc.bx_user WHERE uid<1999 AND usertype=1 AND state=1 LIMIT %d'%(y*3))

    userdata = my_cur.fetchall()
    if userdata:
        user = userdata[(y-1)*2] if len(userdata)>(y-1)*2 else userdata[-1]
        return user

def main():
    #指定最大时间间隔,默认1000s,指定重试次数,默认3,指定onlineaskid,默认0
    t,n,onlineaskid = 1000,3,0
    #随机获取一个时间间隔值和limit的条数
    x = random.randrange(101, t, 101)
    y = random.randrange(1, 15, 1)
    time.sleep(x)
    Time = int(time.time())
    my_cxn = MySQLdb.connect(**mysql_conf)
    my_cur = my_cxn.cursor()
    my_cur.execute('SELECT askid,ask_content FROM bx_caiji.bx_ask WHERE askid>15000 AND online_time<%d LIMIT %d'%(Time-86400*30,y*3))
    data = my_cur.fetchall()
    #随机抽取一个问题和用户完成提问
    Data = data[(y-1)*2]
    uid = get_ask_user(my_cur,y,Time)

    ###将用户的uid,问题内容,安全码组成一个字典####
    DAta={'uid':uid['uid'],'content':Data['ask_content'],'secret':'gc7232275'}
    url='https://www.bao361.cn/ask/auto_add_ask/'

    ###每问题尝试提交3次，如果连续3次提交都不成功，则放弃提交该问题###
    while n :
        DATA=post_ask(url,DAta,Time)
        D = json.loads(DATA.content)
        if D.get('status',0) :
            onlineaskid = D.get('askid',0)
            break
        else :
            F = open('/tmp/auto_ask_ans.log', 'a')
            F.write(str(Time)+'            '+str(D) + '\n')
            F.close()
            time.sleep(y)
            n = n -1

    if Data['askid']:
        my_cur.execute('UPDATE bx_caiji.bx_ask SET online_time=%d,online_askid=%d,uid=%d WHERE askid=%d'%(Time,onlineaskid,uid['uid'],Data['askid']))
    my_cxn.commit()
    my_cur.close()
    my_cxn.close()

if __name__ == '__main__':
    main()
