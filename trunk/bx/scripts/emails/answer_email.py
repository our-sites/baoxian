#! /usr/bin/env python
# coding:utf-8
# --------------------------------
# Created by coco  on 2017/9/20
# ---------------------------------
# Comment: 主要功能说明: 有用户问问题是,及时通知
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from pyh import *
import MySQLdb
import time,datetime,os
import smtplib
import traceback
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

def do_op_db(sql):
    conn_mysql = MySQLdb.connect(host='118.89.220.36',user='mha_user',passwd='gc895316',db='bx_abc',charset='utf8')
    cur = conn_mysql.cursor()
    cur.execute(sql)
    rs = cur.fetchall()
    return rs

# 更新数据库表记录
def up_db_tab(sql):
    conn_mysql = MySQLdb.connect(host='118.89.220.36',user='mha_user',passwd='gc895316',db='bx_abc',charset='utf8')
    cur = conn_mysql.cursor()
    cur.execute(sql)
    conn_mysql.commit()
    cur.close()
    conn_mysql.close()

# 获取本月第一天的时间戳
def get_month_timestamp():
    NowYear = time.localtime()[0]
    NowMonth = time.localtime()[1]
    # LastMonth = NowMonth - 1
    # if NowMonth == 1:
    #     LastMonth = 12
    #     NowYear = NowYear -1
    result = "%s-%s-%d" % (NowYear, NowMonth, 1)
    TimeStamp=time.mktime(time.strptime(result,'%Y-%m-%d')) #日期转换为时间戳
    # LocalTime = time.localtime(TimeStamp)#将日期时间戳转换为localtime
    return   TimeStamp

# send email to users
def sendmail(msg):
    '''''
    @subject:邮件主题
    @msg:邮件内容
    @toaddrs:收信人的邮箱地址
    @fromaddr:发信人的邮箱地址
    @smtpaddr:smtp服务地址，可以在邮箱看，比如163邮箱为smtp.163.com
    @password:发信人的邮箱密码
    '''
    fromaddr = "lantian_929@163.com"
    smtpaddr = "smtp.163.com"
    toaddrs = ["120890945@qq.com",
               "943489924@qq.com",
               "271728979@qq.com",
               "505972916@qq.com",
               "290579323@qq.com",
               "287112491@qq.com",
               "136177121@qq.com",
               "517056585@qq.com"]
    subject = "work_base成员: 现有代理人回答问题,请关注该代理人。。。。。。"
    password = "lantian929?"

    mail_msg = MIMEMultipart()
    if not isinstance(subject,unicode):
        subject = unicode(subject, 'utf-8')
    mail_msg['Subject'] = subject
    mail_msg['From'] =fromaddr
    mail_msg['To'] = ','.join(toaddrs)
    mail_alternative = MIMEMultipart('alternative')
    mail_msg.attach(mail_alternative)
    # html格式
    mail_alternative.attach(MIMEText(msg, 'html', 'utf-8'))

    try:
        s = smtplib.SMTP()
        s.connect(smtpaddr)  #连接smtp服务器
        s.login(fromaddr,password)  #登录邮箱
        s.sendmail(fromaddr, toaddrs, mail_msg.as_string()) #发送邮件
        s.quit()
    except Exception,e:
       print "Error: unable to send email"
       print traceback.format_exc()

# 结果转化成html
def to_html(list1,list2):
    page = PyH('new mail')
    page<<'<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
    page<<'<font  >&nbsp;&nbsp;&nbsp;&nbsp;HI:all</font>'
    page<<div(style="text-align:left")<<h4('&nbsp;&nbsp;&nbsp;&nbsp; you have a user answer question !')

    page<<div(style="text-align:center")<<h4('Answers total information')
    mytab = page << table(border="1",cellpadding="3",cellspacing="0",style="margin:auto")
    tr3 = mytab << tr(bgcolor="lightgrey")
    tr3 << th('ans_count_month') +th('ans_total')
    for i in range(len(list1)):
        tr4 = mytab << tr()
        for j in range(2):
            tr4 << td(list1[i][j])

    page<<div(style="text-align:center")<<h4('New Answers info')
    mytab = page << table(border="1",cellpadding="3",cellspacing="0",style="margin:auto")
    tr1 = mytab << tr(bgcolor="lightgrey")
    tr1 << th('ansid') + th('askid')+th('ans_content') +th('uid') + th('ans_time')
    for i in range(len(list2)):
        tr2 = mytab << tr()
        for j in range(5):
            tr2 << td(list2[i][j])
            if list2[i][j]==' ':
                tr2.attributes['bgcolor']='yellow'
            if list2[i][j]=='':
                tr2[1].attributes['style']='color:red'
    return page.printOut('ans.html')

if __name__ == '__main__':

    # 查询有uid>3000的用户 有自助注册用户提问问题则发邮件,否则pass
    max_ansid = do_op_db(sql=' select max(ansid) from bx_answer where uid>3000 ')[0][0]
    print "max_ansid = " + str(max_ansid)


    # 获取 email_mark_tab表中的 上次执行的时间戳标记 mark_time
    mark_id = do_op_db(sql = ''' select mark_id from email_mark_tab where email_name='answer_email'  ''' )[0][0]
    print "mark_id = " + str(mark_id)

    if int(mark_id) < int(max_ansid):
        ask_info = do_op_db(sql=' select ansid,askid,ans_content,uid,ans_time from bx_answer where uid>3000 and ansid>%d '%int(mark_id))

        if len(ask_info)>0:
            ans_info_list = []
            for i in ask_info:
                ansid = i[0]
                askid = i[1]
                ans_content = i[2]
                uid = i[3]
                ans_time = i[4]
                # 转换addtime为时间格式
                ans_datetime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(ans_time))

                ans_info = [ansid,askid,ans_content,uid,ans_datetime]
                ans_info_list.append(ans_info)

            print ans_info_list
            # 当月新增用户数量
            # 获取本月第一天的时间戳
            month_time = int(get_month_timestamp())
            # print month_time
            ans_count_month = do_op_db(sql = 'select count(*) from bx_answer where uid>3000 and ans_time<%d '%month_time)[0]
            print "本月用户自主回答次数: " + str(ans_count_month[0])

            # 回答总数
            ans_total = do_op_db(sql = 'select count(*) from bx_answer where uid>3000 ')[0]
            print "总回答次数为: " + str(ans_total[0])

            ans_total_info_list = [[ans_count_month[0],ans_total[0]]]
            print    ans_total_info_list

            to_html(list1=ans_total_info_list,list2=ans_info_list)

            htmlfile = open('ans.html')
            htmlText = htmlfile.read()
            msg = htmlText
            sendmail(msg)
            htmlfile.close()

        else:
            print "没有自主用户新回答。。。。"
            pass

        # 更新mark_time的值,为下次查询做准备
        print max_ansid
        up_db_tab(sql = ''' update email_mark_tab set mark_id =%d where email_name = 'answer_email'  '''%max_ansid)


    else:
        print "没有新回答!"