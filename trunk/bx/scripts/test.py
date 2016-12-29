#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/11.
# ---------------------------------

import  urllib2
import  urllib

# img_content=open("./baidu.png","rb").read()
#
# a=open("baidu1.png","wb")
# a.write(img_content)
# a.close()
#
# a=urllib2.urlopen("http://img.baoxiangj.com/api/upload_img",data=urllib.urlencode({"extname":".png","file":img_content}) )
# #使用说明：
# # 地址：  http://img.baoxiangj.com/api/upload_img
# # 传参形式： post
# # 参数： file  文件内容
# # 参数： extname 文件的扩展名
# # 返回数据如下：
# #  {"status": true, "imgurl": "/media/img/2885cdb57f913ed832df4a0731bdc765.png", "filename": "2885cdb57f913ed832df4a0731bdc765.png"}
# #  imgurl 为这个文件的访问地址
# #  filename 为这个文件在服务器中的文件名
# print a.read()
from gcutils.db import  MySQLMgr
from itertools import groupby
# mgr=MySQLMgr("113.10.195.169",3306,"bx_abc","bx_user","gc895316")

# result= mgr.runQuery("select bx_type from bx_product ",())
# data=[]
# for i in result:
#     _=i[0].split(",")
#     print _
#     for  j  in _:
#         try:
#             data.append(int(j))
#         except:
#             pass
# data.sort()
# print data
# for t,k in groupby(data):
#     print t,len([_  for _ in k ])
# result=mgr.runQuery("select cid,count(*) as num  from bx_proxyuser_profile group by cid  order by num desc ",())
# for i ,j in result:
#     print i,j
#     mgr.runOperation("update bx_company set dailiren_weight =%s WHERE cid=%s",(j,i))
mgr=MySQLMgr("192.168.8.94",3306,"shuili","root","gc895316")
print mgr.runQuery('''SELECT title,author,source,publist_date,source_database,quote_times,
download_times,teacher,author_info,abstract,abstract_en,keyword,
keyword_en,network_publisher,network_publish_date,cate_num,from_url from zhiwang_article_shuishabianhua WHERE title
like \'%%黄河%%\'''',()).__len__()

