#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/14.
# ---------------------------------
import  urllib2
import  urllib
import  json
request=urllib2.Request("http://tva1.sinaimg.cn/crop.24.185.402.402.180/bbc4d8bbtw1e974nf5ltuj20dy0imagi.jpg")
request.headers["User-Agent"]="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.202 Safari/537.36"
request.headers["Accept"]="text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
request.headers["Accept-Encoding"]="gzip, deflate"
request.headers["Progma"]="no-cache"
result= urllib2.urlopen(request).read()
a=open("aaa.jpg","wb")
a.write(result)
a.close()
