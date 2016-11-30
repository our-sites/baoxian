#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/11/25.
# ---------------------------------
from threadspider import   *

#spider_init(5,10000000)
import  requests
r=requests.post("http://218.249.40.252/kns55/request/SearchHandler.ashx",{"action":"undefined",
                                                                        "NaviCode":"*",
                                                                        "PageName":"ASP.brief_result_aspx",
                                                                        "DbPrefix":"SCDB",
                                                                        "DbCatalog":"中国学术文献网络出版总库",
                                                                        "ConfigFile":"SCDB.xml",
                                                                        "db_opt":"中国学术文献网络出版总库",
                                                                        "db_value":"中国期刊全文数据库,中国博士学位论文全文数据库,中国优秀硕士学位论文全文数据库,中国重要会议论文全文数据库,中国重要报纸全文数据库",
                                                                        "txt_1_sel":"全文",
                                                                        "txt_1_value1":"黄河",
                                                                        "his":"0",
                                                                        })
print r.headers
print r.text
import  urllib2
import  urllib
for i in range(0,10000):
    headers={"Cookie":"ASP.NET_SessionId=3gvpte45ovg31s45l3n3jv45; LID=; CurTop10KeyWord=%2c%u9ec4%u6cb3; RsPerPage=20; FileNameS=cnki%3A"}
    r=requests.post("http://218.249.40.252/kns55/brief/brief.aspx?curpage=%s&RecordsPerPage=20&QueryID=0&ID=&turnpage=1&tpagemode=L&dbPrefix=SCDB&Fields=&DisplayMode=listmode&PageName=ASP.brief_result_aspx&sKuaKuID=0"%i,
                  headers=headers)
    print i
    print r.text[:50]