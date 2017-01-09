#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/14.
# ---------------------------------
import  urllib2


import  pyquery

import  urllib2
import  urllib
import  requests
import time
print time.time()
data=requests.post("http://iir.circ.gov.cn/web/baoxyx!searchInfoBaoxyx.html",{"id_card":"","certificate_code":"00201412110000069878","evelop_code":"",
                                                                              "name":"","valCode":""},timeout=30)

print time.time()
doc=pyquery.PyQuery(data.content.decode("gbk"))
print doc.html()
