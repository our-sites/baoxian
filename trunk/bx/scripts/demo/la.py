#coding:utf-8


from threadspider import  *
from pyquery import *
import  json
spider_init(50,1000000)
result_file=open('output.txt',"w")
for i in range(1,1000):
    if i==1:
        url="http://top.chinaz.com/all/index_alexa.html"
    else:
        url="http://top.chinaz.com/all/index_alexa_%s.html"%i
    def handle(data):
        doc=PyQuery(data)
        for i in doc(".col-gray"):
            domain= PyQuery(i).html()
            if "." in domain:
                _d=domain.split(".")[-2]
                #print _d
                _url="https://wss.qcloud.com/buy/api/domains/domain/check?g_tk=&t=1352121016&_format=json&mc_gtk=&domain_name=%s&tlds=.la"%_d
                def _handle(data):
                    try:
                        data=json.loads(data)
                        result=data["result"]
                        _a,_b= result["domain"],result["reged"]
                        if not _b:
                            print _a
                            result_file.write(_a+"\n")
                            result_file.flush()
                    except:
                        pass
                Spider(_url,response_handle=_handle,timeout=300)

    Spider(url,response_handle=handle,code="utf-8",timeout=300)
spider_join()
result_file.close()


# chuanke.la
# zhifang.la
# tenpay.la
# 9game.la