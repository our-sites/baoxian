#! /usr/bin/env python
# coding:utf-8
# --------------------------------
# Created by coco  on 2017/9/9
# ---------------------------------
# Comment: 主要功能说明
# 监控到新注册用户,发邮件给相关人的邮箱。
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

# qq邮箱授权码
_pwd='zpgflkiksbxibggf'

def get_userinfo(sql):
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
    subject = "恭喜您,您有新用户注册。。。"
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
def to_html(month_userinfo_list,new_userinfo_list):
    page = PyH('new mail')
    page<<'<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
    page<<'<font  >&nbsp;&nbsp;&nbsp;&nbsp;HI:all</font>'
    page<<div(style="text-align:left")<<h4('&nbsp;&nbsp;&nbsp;&nbsp; congratulation   !!!! ')
    page<<div(style="text-align:left")<<h4('&nbsp;&nbsp;&nbsp;&nbsp; you have a new user sign in.')
    page<<'<font color="#a52a2a"  >&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; is_proxy is flag :1 dailiren  0 toubaoren.</font>'
    page<<div(style="text-align:center")<<h4('The total information')
    mytab = page << table(border="1",cellpadding="3",cellspacing="0",style="margin:auto")
    tr3 = mytab << tr(bgcolor="lightgrey")
    tr3 << th('month_count') +th('dailiren_month_count')+th('toubaoren_month_count')+ th('total_count')
    for i in range(len(month_userinfo_list)):
        tr4 = mytab << tr()
        for j in range(4):
            tr4 << td(month_userinfo_list[i][j])

    page<<div(style="text-align:center")<<h4('new user info')
    mytab = page << table(border="1",cellpadding="3",cellspacing="0",style="margin:auto")
    tr1 = mytab << tr(bgcolor="lightgrey")
    tr1 << th('uid') + th('username')+th('real_name') +th('phone') + th('wechat') +th('is_proxy')+th('addtime')
    for i in range(len(new_userinfo_list)):
        tr2 = mytab << tr()
        for j in range(7):
            tr2 << td(new_userinfo_list[i][j])
            if new_userinfo_list[i][j]==' ':
                tr2.attributes['bgcolor']='yellow'
            if new_userinfo_list[i][j]=='':
                tr2[1].attributes['style']='color:red'
    return page.printOut('dailiren.html')

if __name__ == '__main__':

    # 查询有新用户注册则发邮件,否则pass
    max_uid = get_userinfo(sql='select max(uid) from bx_user where uid>3000')[0][0]
    print "max_uid = " + str(max_uid)

    # 获取email_mark_tab表中dailiren 的标记mark_uid
    mark_uid =  get_userinfo(sql='''select mark_id from email_mark_tab where email_name='dailiren_email' ''')[0][0]
    print "mark_uid = " +str(mark_uid)

    if int(mark_uid) < int(max_uid):
        userinfo = get_userinfo(sql='select uid,username,real_name,phone,qq,email,weixin,is_proxy,addtime from bx_user where uid>%s'%mark_uid)
        user_count = len(userinfo)

        if user_count>0:
            new_userinfo_list = []
            for i in userinfo:
                uid = i[0]
                username = i[1]
                real_name = i[2]
                phone = i[3]
                weixin = i[6]
                is_proxy = i[7]
                addtime = i[8]
                # 转换addtime为时间格式
                addtime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(addtime))
                # new_userinfo = {"uid":uid,"username":username,"real_name":real_name,"phone":phone,"weixin":weixin,"addtime":addtime}
                new_userinfo = [uid,username,real_name,phone,weixin,is_proxy,addtime]
                new_userinfo_list.append(new_userinfo)
            print new_userinfo_list

            # 获取本月第一天的时间戳
            month_time = int(get_month_timestamp())
            # print month_time
            user_count_month = get_userinfo(sql = ' select count(*) from bx_user where addtime>=%s '%month_time)[0]
            print "本月用户数量为: " + str(user_count_month[0])

            # 本月代理人注册数
            dailiren_month_count = get_userinfo(sql = ' select count(*) from bx_user where addtime>=%s and is_proxy=1 '%month_time)[0]

            # 本月投保人注册数
            toubaoren_month_count =  get_userinfo(sql = ' select count(*) from bx_user where addtime>=%s and is_proxy=0 '%month_time)[0]


            # 总计用户数
            user_total = get_userinfo(sql = 'select count(*) from bx_user where uid>3000 ')[0]
            print "总用户数量为: " + str(user_total[0])

            month_userinfo_list = [[user_count_month[0],dailiren_month_count[0],toubaoren_month_count[0],user_total[0]]]
            print    month_userinfo_list

            # 生成html文件
            to_html(month_userinfo_list,new_userinfo_list)
            htmlfile = open('dailiren.html')
            htmlText = htmlfile.read()

            print htmlText

            msg = htmlText
            sendmail(msg)
            htmlfile.close()

        else:
            print "没有新用户注册."
            # logfile = open('run.log','a')
            # logfile.write('====================================='+'\n'+'没有新用户注册.'+'\n')
            # logfile.close()
            pass

        # 更新mark_uid的值
        up_db_tab(sql=''' update bx_abc.email_mark_tab set mark_id=%d where email_name='dailiren_email' '''%max_uid)
    else:
        print "max_uid = mark_uid pass!!!"
