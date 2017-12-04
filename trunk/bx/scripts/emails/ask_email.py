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
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkdysmsapi.request.v20170525 import QuerySendDetailsRequest
from aliyunsdkcore.client import AcsClient
import uuid,json


# qq邮箱授权码
_pwd='zpgflkiksbxibggf'

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
    subject = "尊敬的管家代理人：您有用户提问问题，请及时回复。。。"
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
def to_html(ask_info_list,ask_total_info_list,dailiren_mess_info_list):
    page = PyH('ask mail')
    page<<'<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
    page<<'<font  >&nbsp;&nbsp;&nbsp;&nbsp;HI:all</font>'
    page<<div(style="text-align:left")<<h4('&nbsp;&nbsp;&nbsp;&nbsp; you have a new question .')
    page<<div(style="text-align:center")<<h4('Question total information')
    mytab = page << table(border="1",cellpadding="3",cellspacing="0",style="margin:auto")
    tr3 = mytab << tr(bgcolor="lightgrey")
    tr3 << th('ask_count_month') +th('ask_total')
    for i in range(len(ask_total_info_list)):
        tr4 = mytab << tr()
        for j in range(2):
            tr4 << td(ask_total_info_list[i][j])

    page<<div(style="text-align:center")<<h4('new questions info')
    mytab = page << table(border="1",cellpadding="3",cellspacing="0",style="margin:auto")
    tr1 = mytab << tr(bgcolor="lightgrey")
    tr1 << th('askid') + th('ask_title')+th('ask_content') +th('uid') + th('ask_time')+th('province')+th('city')+th('url')
    for i in range(len(ask_info_list)):
        tr2 = mytab << tr()
        for j in range(8):
            tr2 << td(ask_info_list[i][j])
            if ask_info_list[i][j]==' ':
                tr2.attributes['bgcolor']='yellow'
            if ask_info_list[i][j]=='':
                tr2[1].attributes['style']='color:red'

    page<<div(style="text-align:center")<<h4('send message to the dailiren list')
    mytab = page << table(border="1",cellpadding="3",cellspacing="0",style="margin:auto")
    tr1 = mytab << tr(bgcolor="lightgrey")
    tr1 << th('username') + th('real_name')+th('phone')
    for i in range(len(dailiren_mess_info_list)):
        tr2 = mytab << tr()
        for j in range(3):
            tr2 << td(dailiren_mess_info_list[i][j])
            if dailiren_mess_info_list[i][j]==' ':
                tr2.attributes['bgcolor']='yellow'
            if dailiren_mess_info_list[i][j]=='':
                tr2[1].attributes['style']='color:red'
    return page.printOut('ask.html')

# 给同城的代理人发短信通知
"""
短信产品-发送短信接口
Created on 2017-06-12
"""
REGION = "cn-hangzhou"# 暂时不支持多region
# ACCESS_KEY_ID/ACCESS_KEY_SECRET 根据实际申请的账号信息进行替换
ACCESS_KEY_ID = "LTAIzfDlLirkJDAL"
ACCESS_KEY_SECRET = "V6Fd5EaQxGimQgHlwxXKNVAQMITxT7"
acs_client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION)
# 请参考本文档步骤2
def send_sms(business_id, phone_number, sign_name, template_code, template_param=None):
    smsRequest = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    smsRequest.set_TemplateCode(template_code)
    # 短信模板变量参数,友情提示:如果JSON中需要带换行符,请参照标准的JSON协议对换行符的要求,比如短信内容中包含\r\n的情况在JSON中需要表示成\\r\\n,否则会导致JSON在服务端解析失败
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)
    # 设置业务请求流水号，必填。
    smsRequest.set_OutId(business_id)
    # 短信签名
    smsRequest.set_SignName(sign_name);
    # 短信发送的号码，必填。支持以逗号分隔的形式进行批量调用，批量上限为1000个手机号码,批量调用相对于单条调用及时性稍有延迟,验证码类型的短信推荐使用单条调用的方式
    smsRequest.set_PhoneNumbers(phone_number)
    # 发送请求
    smsResponse = acs_client.do_action_with_exception(smsRequest)
    return smsResponse


# 获取同城市代理人信息,并发短信通知。如果同城市代理人信息为空,则发送全国代理人 ,目前限制数量选取5个发送
def send_mess_to_dailiren(province_id,city_id,askid,city):
    # 根据province_id,city_id获取askid不同的提问者所在的省份和城市,用于提取相关同城的代理人信息。
    #获取 提问者所在的省份和城市信息后,获取同城市的代理人信息
    dailiren_info = do_op_db(sql='select uid,username,real_name,phone,qq,weixin from bx_user where uid>3000 and is_proxy=1 and (province_id=%s or  city_id=%s) limit 5 ;'%(province_id,city_id))
    # 已发送短信的代理人列表信息
    dailiren_mess_info_list=[]
    if len(dailiren_info) >0:
        for m in dailiren_info:
            username=m[1]
            real_name=m[2]
            phone=m[3]

            # 绍功电话,gq电话
            #phone="18135783938"
            #phone="15038311400"
            # 获取username,askid,city 给同城代理人发短信
            if len(real_name)>0:
                params={'username':real_name ,'city':city,'askid':askid}
            else:
                params={'username':username ,'city':city,'askid':askid}
            print phone,params
            send_sms(__business_id, phone, "保险管家", "SMS_112465067", json.dumps(params))
            dailiren_mess_info=[username,real_name,phone]
            dailiren_mess_info_list.append(dailiren_mess_info)

    else:
        all_dailiren_info = do_op_db(sql='select uid,username,real_name,phone,qq,weixin from bx_user where uid>3000 and is_proxy=1 limit 5 ;')
        for n in  all_dailiren_info:
            username = n[1]
            real_name = n[2]
            phone = n[3]

            # 获取username,askid,city 给同城代理人发短信
            if len(real_name)>0:
                params={'username':real_name ,'city':city,'askid':askid}
            else:
                params={'username':username ,'city':city,'askid':askid}
            print phone,params
            send_sms(__business_id, phone, "保险管家", "SMS_112465067", json.dumps(params))
            dailiren_mess_info=[username,real_name,phone]
            dailiren_mess_info_list.append(dailiren_mess_info)
    return dailiren_mess_info_list

def main():
    # 查询有新用户提问问题则发邮件,否则pass
    max_askid = do_op_db(sql='select max(askid) from bx_ask where uid>3000;')[0][0]
    print "max_askid = " + str(max_askid)
    # 获取 email_mark_tab 表中的 mark值
    mark_id = do_op_db(sql = '''select mark_id from email_mark_tab where email_name='ask_email'  ''')[0][0]
    print "mark_id= " + str(mark_id)
    if int(mark_id) < int(max_askid):
        ask_info = do_op_db(sql=' select askid,ask_title,ask_content,uid,ask_time,(select areaname from area where id=province) province_name,(select areaname from area where id=city) city_name,province,city from bx_ask where uid>3000 and askid>%s and mark=0 ;'%int(mark_id))

        if len(ask_info)>0:
            ask_info_list,ask_area_info_list=[],[]
            for i in ask_info:
                print i
                askid = i[0]
                ask_title = i[1]
                ask_content = i[2]
                uid = i[3]
                ask_time = i[4]
                province = i[5]
                city =i[6]
                url = 'https://www.bao361.cn/ask/detail/%s.html'%askid
                province_id=i[7]
                city_id=i[8]
                # 转换addtime为时间格式
                ask_datetime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(ask_time))

                ask_info = [askid,ask_title,ask_content,uid,ask_datetime,province,city,url]
                ask_info_list.append(ask_info)

                # 调用发短信的函数
                dailiren_mess_info_list = send_mess_to_dailiren(province_id,city_id,askid,city)

            # 获取本月第一天的时间戳
            month_time = int(get_month_timestamp())
            print month_time
            ask_count_month = do_op_db(sql = ' select count(*) from bx_ask where uid>3000 and ask_time>%d and mark=0; '%month_time)[0]
            print "本月用户自主提问次数: " + str(ask_count_month[0])

            # 提问问题总数
            ask_total = do_op_db(sql = 'select count(*) from bx_ask where uid>3000 and mark=0;')[0]
            print "总用户数量为: " + str(ask_total[0])

            ask_total_info_list = [[ask_count_month[0],ask_total[0]]]
            print    ask_total_info_list

            to_html(ask_info_list,ask_total_info_list,dailiren_mess_info_list)

            htmlfile = open('ask.html')
            htmlText = htmlfile.read()

            print htmlText

            #给运营人员发邮件
            msg = htmlText
            sendmail(msg)
            htmlfile.close()

        else:
            print "没有自主用户提问新问题。。。。"
            pass

        # 更新ask_max_askid的值,为下次查询做准备
        print  max_askid
        up_db_tab(sql = ''' update email_mark_tab set mark_id =%d where email_name = 'ask_email'  '''%max_askid)
    else:
        print "没有新问题!"

if __name__ == '__main__':
    __business_id = uuid.uuid1()
    print __business_id
    start_time=datetime.datetime.now()
    print "开始执行时间:" + str(start_time)
    main()
    end_time=datetime.datetime.now()
    print "结束时间:" + str(end_time)
