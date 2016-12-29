#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/11/25.
# ---------------------------------
from threadspider import   *
from pyquery import  PyQuery
import  re
from threading import  Lock
from gcutils.db  import  MySQLMgr

mgr=MySQLMgr("192.168.8.94",3306,"shuili","root","gc895316")

lock=Lock()
spider_init(22,10000000)
for i in range(1,221):
    def handle(data):
        doc=PyQuery(data)
        print data[:100]
        #print doc(".GridTableContent")
        lock.acquire()
        for j in doc(".GridTableContent").find("tr[bgcolor]"):
            from_url=PyQuery(PyQuery(j).find("a")[-1]).attr("href")
            from_url="http://218.249.40.252"+from_url
            for a,b,c,d,e,f,g in [PyQuery(j).find("td")[-7:]]:
                title=re.search(r"ReplaceJiankuohao\('(.+?)'\)\)\)\)",PyQuery(a).find("a").html()).groups()[0]
                author=PyQuery(b).text()
                source=PyQuery(c).text()
                publist_date=PyQuery(d).text()
                try:
                    publist_date=re.search(r"(\d{4}-\d{2}-\d{2})",publist_date).groups()[0]
                except:
                    publist_date=""
                from_database=PyQuery(e).text()
                quote_times=PyQuery(f).text()
                download_times=PyQuery(g).text()
                if quote_times:
                    quote_times=int(quote_times.strip())
                else:
                    quote_times=0
                if download_times:
                    download_times=int(download_times.strip())
                else:
                    download_times=0
                print title,author,source,publist_date,from_database,quote_times,download_times,from_url
                mgr.runOperation('''insert ignore  into zhiwang_article_shuishabianhua( title, author, source, publist_date, source_database,
                                    quote_times, download_times, from_url)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s)''',
                                 (title,author,source,publist_date,from_database,quote_times,download_times,from_url))
        lock.release()

    Spider("http://218.249.40.252/kns55/brief/brief.aspx?curpage=%s&RecordsPerPage=20&QueryID=1127&ID=&turnpage=1&tpagemode=L&dbPrefix=SCDB&Fields=&DisplayMode=listmode&PageName=ASP.brief_result_aspx&sKuaKuID=1127"%i,code="utf-8",
           cookie="RsPerPage=20; ASP.NET_SessionId=mgrhqgudezz2zmvkqruayz2p; CurTop10KeyWord=%2c%u9ec4%u571f%u9ad8%u539f%2c%u6c34%u6c99%u53d8%u5316; LID=; KNS_DisplayModel=; FileNameS=cnki%3A",
           handle=handle,timeout=20
           )
spider_join()