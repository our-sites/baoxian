#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/14.
# ---------------------------------

from threadspider import  *
from pyquery import  *
import urllib

spider_init(3,1000000)
result=[]
def some_day(date):
    def handle(data):
        doc=PyQuery(data)
        postdata={"_ASYNCPOST":"true","__EVENTARGUMENT":"","__EVENTTARGET":"",
                  "ctl00$ScriptManager1":"ctl00$ScriptManager1|ctl00$ContentLeft$Button1",
                  "__VIEWSTATE":doc("#__VIEWSTATE").attr("value").encode("utf-8"),
                  "ctl00$ContentLeft$menuDate1$TextBox11":date,
                  "__VIEWSTATEGENERATOR":doc("#__VIEWSTATEGENERATOR").attr("value").encode("utf-8"),
                  "__EVENTVALIDATION":doc("#__EVENTVALIDATION").attr("value").encode("utf-8"),
                  "ctl00$ContentLeft$Button1":u"查询".encode("utf-8")
                  }
        def content_handle(data,date=date):
            doc=PyQuery(data)
            _kk=[]
            for i in doc("tr[align]:not(.tableTitle)"):
                _tt=[]
                for j in PyQuery(i).find("td"):
                    _tt.append(PyQuery(j).html())
                _kk.append(_tt)
            result.append([date,_kk])
        Spider("http://61.163.88.227:8006/hwsq.aspx",code="utf-8",handle=content_handle,data=urllib.urlencode(postdata),
               header={"X-Requested-With":"XMLHttpRequest",
                       "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
                       "Referer":"http://61.163.88.227:8006/hwsq.aspx",
                       "Accept-Language":"zh-CN,zh;q=0.8",
                       "Accept":"*/*",
                       "User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/5.7.15702.19 Safari/537.36",
                       "Origin":"http://61.163.88.227:8006",
                       "Host":"61.163.88.227:8006"})
    Spider("http://61.163.88.227:8006/hwsq.aspx?aa="+date ,code="utf-8",handle=handle)
now=datetime.datetime.now()
for i in range(0,30):
    _u=now-datetime.timedelta(days=i)
    some_day(_u.strftime("%Y-%m-%d"))
spider_join()
output=open("output.txt","w")
result.sort(key=lambda x:x[0])
for i,j in result:
    output.write("################################\n")
    output.write("##########%s############\n"%i)
    for m in j:
        for t in m:
            output.write(t+",")
        output.write("\n")
    output.write("\n")
output.flush()
output.close()