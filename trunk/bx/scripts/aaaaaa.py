#coding:utf-8
import re
a=u"据中国红薯价格网统计：2016年6月22日全国甜玉米价格如下：山西晋善晋美农产品批发市场-甜玉米：2.05元/斤"
result= re.search(ur"(\d{4}年\d{1,2}月\d+日)全国(.+?)价格如下：(.+?)晋善.+?：(.+?元/斤)",a).groups()
for i in result:
    print i

import time
import threading
from threading import RLock
import os

file_obj=open("test.txt","w")

lock=RLock()
def fun(x):
    print "sleep %s start"%x
    lock.acquire()
    print "lock acquire"
    file_obj.write("xxxxx\n")
    lock.release()
    print "lock release"
    time.sleep(x)
    print "sleep %s end"%x

thread=threading.Thread(target=fun,args=(3,))
thread_2=threading.Thread(target=fun,args=(4,))
print time.time()
thread.start()
thread_2.start()
raw_input("")
<div class="bdsharebuttonbox"><a href="#" class="bds_more" data-cmd="more"></a><a href="#" class="bds_qzone" data-cmd="qzone" title="分享到QQ空间"></a><a href="#" class="bds_tsina" data-cmd="tsina" title="分享到新浪微博"></a><a href="#" class="bds_tqq" data-cmd="tqq" title="分享到腾讯微博"></a><a href="#" class="bds_renren" data-cmd="renren" title="分享到人人网"></a><a href="#" class="bds_weixin" data-cmd="weixin" title="分享到微信"></a></div>
<script>window._bd_share_config={"common":{"bdSnsKey":{},"bdText":"","bdMini":"2","bdMiniList":false,"bdPic":"","bdStyle":"1","bdSize":"24"},"share":{},"image":{"viewList":["qzone","tsina","tqq","renren","weixin"],"viewText":"分享到：","viewSize":"16"},"selectShare":{"bdContainerClass":null,"bdSelectMiniList":["qzone","tsina","tqq","renren","weixin"]}};with(document)0[(getElementsByTagName('head')[0]||body).appendChild(createElement('script')).src='//static/js/bd_share.js?cdnversion='+~(-new Date()/36e5)];</script>
