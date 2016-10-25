#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/11.
# ---------------------------------

import urllib2,urllib
import  datetime
import  json
from gcutils.encrypt import  md5

def send_dayysms_validnumber(phone,content):
    req=urllib2.Request("http://gw.api.taobao.com/router/rest")
    req.headers["Content-Type"]="application/x-www-form-urlencoded;charset=utf-8"
    _u={"app_key":"23475993",
                         "format":"json",
                         "method":"alibaba.aliqin.fc.sms.num.send",
                         "timestamp":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                         "v":"2.0",
                         "sign_method":"md5",
                         "sms_type":"normal",
                         "sms_free_sign_name":"保险管家",
                         "rec_num":str(phone),
                         "sms_template_code":"SMS_17260018",
                         "sms_param":json.dumps({"number":content},ensure_ascii=True),
                         }
    sortinfo=sorted( _u.items() ,key=lambda x:x[0])
    _t=""
    for i,j in sortinfo:
        _t+=(i+j)
    _u["sign"]=md5("318f348879b9e2b7ac830c5db168eb57"+_t+"318f348879b9e2b7ac830c5db168eb57").upper()
    data=urllib2.urlopen(req,urllib.urlencode(_u)).read()
    return json.loads(data)

#print send_dayysms_validnumber(15903992399,"123456")["alibaba_aliqin_fc_sms_num_send_response"]["result"]["success"]