#! /usr/bin/env python
#coding=utf-8
__author__ = 'Administrator'
#this is SVN_CODE
#create by 2017/05/25 0023
"""水军伪装代理人回答问题"""

import MySQLdb,MySQLdb.cursors
import time
import random
import re
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

def get_answer(my_cur,D,Time):
    """由问题从数据库随机抽取答案"""
    answer,online_ansid,uidlist = {},'',''
    #获取该问题已有答案的情况
    my_cur.execute('SELECT uid,online_ansid FROM bx_caiji.bx_answer WHERE askid=%d ' % D['askid'])
    Userdata = my_cur.fetchall()
    for U in Userdata :
        if U['online_ansid'] :
            online_ansid=online_ansid+str(U['online_ansid'])+','
        if U['uid'] :
            uidlist=uidlist+str(U['uid'])+','
    #根据该问题已回答的情况决定如何获取新答案
    if online_ansid :
        my_cur.execute('SELECT ansid,ans_content,company,cid,province_id,city_id FROM bx_caiji.bx_answer WHERE online_time<%d AND askid=%d AND ansid NOT IN (%s) ORDER BY ansid' % ((Time - 30*86400),D['askid'],online_ansid[:-1]))
    else :
        my_cur.execute('SELECT ansid,ans_content,company,cid,province_id,city_id FROM bx_caiji.bx_answer WHERE online_time<%d AND askid=%d ORDER BY ansid' % ((Time - 30*86400),D['askid']))
    answer = my_cur.fetchone()
    return answer,uidlist[:-1]

def get_proxy_user(my_cur,answer,uidlist):
    if uidlist:
        my_cur.execute('SELECT uid,phone  FROM bx_user WHERE uid > 1999 AND uid < 3000 AND usertype = 2 AND state = 1 AND city_id=%d AND proxy_cid=%d AND uid NOT IN (%s)  LIMIT 15'%(answer['city_id'],answer['cid'],uidlist))
        userdata = my_cur.fetchall()
        if userdata :
            return userdata
        my_cur.execute( 'SELECT uid,phone  FROM bx_user WHERE uid > 1999 AND uid < 3000 AND usertype = 2 AND state = 1 AND province_id=%d AND proxy_cid=%d AND uid NOT IN (%s)  LIMIT 15'%( answer['province_id'], answer['cid'], uidlist))
        userdata = my_cur.fetchall()
        if userdata :
            return userdata
        my_cur.execute('SELECT uid,phone  FROM bx_user WHERE uid > 1999 AND uid < 3000 AND usertype = 2 AND state = 1 AND uid NOT IN (%s) AND proxy_cid=%d LIMIT 15'%(uidlist, answer['cid']))
        userdata = my_cur.fetchall()
        if userdata:
            return userdata
    else:
        my_cur.execute('SELECT uid,phone  FROM bx_user WHERE uid > 1999 AND uid < 3000 AND usertype = 2 AND state = 1 AND city_id=%d AND proxy_cid=%d LIMIT 15'%(answer['city_id'], answer['cid']))
        userdata = my_cur.fetchall()
        if userdata:
            return userdata
        my_cur.execute('SELECT uid,phone  FROM bx_user WHERE uid > 1999 AND uid < 3000 AND usertype = 2 AND state = 1 AND province_id=%d AND proxy_cid=%d LIMIT 15'%(answer['province_id'], answer['cid']))
        userdata = my_cur.fetchall()
        if userdata:
            return userdata
        my_cur.execute('SELECT uid,phone  FROM bx_user WHERE uid > 1999 AND uid < 3000 AND usertype = 2 AND state = 1 AND proxy_cid=%d LIMIT 15'%answer['cid'])
        userdata = my_cur.fetchall()
        if userdata:
            return userdata
    ###如果以上都没有合适的人选，那就传个默认的###
    my_cur.execute('SELECT uid,phone  FROM bx_user WHERE uid > 1999 AND uid < 3000 AND usertype = 2 AND state = 1 AND proxy_cid=%d LIMIT 15' %answer['cid'])
    userdata = my_cur.fetchall()
    if userdata:
        return userdata

def post_answer(url,Data,Time):
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

def main():
    # 指定最大时间间隔,默认1000s,指定重试次数,默认3,指定onlineaskid,默认0
    t, n, onlineansid,UserData,answer = 1000, 3, 0,[],{}
    #随机获取一个时间间隔值和limit的条数
    x = random.randrange(181, t, 101)
    y = random.randrange(1, 15, 1)
    time.sleep(y)
    Time = int(time.time())
    my_cxn = MySQLdb.connect(**mysql_conf)
    my_cur = my_cxn.cursor()
    if Time%3 :
        my_cur.execute('SELECT askid,online_askid FROM bx_caiji.bx_ask WHERE online_time<%d AND online_askid>436 ORDER BY online_time DESC limit %d'%(Time-x,y*y*10))
    else :
        my_cur.execute('SELECT askid,online_askid FROM bx_caiji.bx_ask WHERE online_time>%d AND online_askid>436 ORDER BY online_time ASC limit %d'%(Time-y*86400,y*y*20))
    data = my_cur.fetchall()

    #随机抽取一个问题，从采集的答案库中抽取答案来完成提问
    for D in data :
        answer,uidlist = get_answer(my_cur,D,Time)
        print answer,D
        if answer :
            break
        else :
            continue

    #如果找到了对应的答案,则进行发布
    if answer :
        # 随机抽取一个代理人,排除同一个问题一个人回答两次的问题
        userdata = get_proxy_user(my_cur,answer,uidlist)
        uid = userdata[0] if len(userdata) == 1 else userdata[Time%len(userdata)]
        #处理回答中夹带的手机号、进行替换处理
        answer['ans_content']=re.sub("1[3|5|7|8]\d{9}",str(uid['phone']),answer['ans_content'])
        url = 'https://www.bao361.cn/ask/auto_add_ans/'
        #组合回答问题的数据字典
        Data={'uid':uid['uid'],'askid':D['online_askid'],'content':answer['ans_content'],'secret':'gc7232275'}
        ###提交3次，如果连续3次提交都不成功，则放弃提交该问题###
        while n:
            DATA = post_answer(url,Data,Time)
            DATA = json.loads(DATA.content)
            if DATA['status']:
                onlineansid = DATA['ansid']
                break
            else:
                F = open('/tmp/auto_ask_ans.log','a')
                F.write(str(Time)+'            '+str(DATA)+'\n')
                F.close()
                time.sleep(y)
                n = n - 1
        if onlineansid :
            my_cur.execute('UPDATE bx_caiji.bx_answer SET online_time=%d,uid=%d,online_ansid=%d WHERE ansid=%s'%(Time,uid['uid'],onlineansid,answer['ansid']))
    my_cxn.commit()
    my_cur.close()
    my_cxn.close()

if __name__ == '__main__':
    main()
