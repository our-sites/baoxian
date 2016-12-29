#coding:utf-8
__author__ = 'zhoukunpeng'
# --------------------------------
# Created by zhoukunpeng  on 2016/9/18.
# ---------------------------------
import  pyquery

from scripts.新闻.threadspider import *

spider_init(30,5000000)  #初始化蜘蛛线程池为30个线程。 队列大小为500万
def dianying(result):   #处理函数
    doc=pyquery.PyQuery(result)
    for index,obj in enumerate(doc(".list-title")):
        rank=index+1
        name=pyquery.PyQuery(obj).text()
        print name

def dianshiju(result):  #处理函数
    doc=pyquery.PyQuery(result)
    for index,obj in enumerate(doc(".list-title")):
        rank=index+1
        name=pyquery.PyQuery(obj).text()
        print name
Spider("http://top.baidu.com/buzz?b=26&c=1&fr=topcategory_c1",code="gbk",handle=dianying)

Spider("http://top.baidu.com/buzz?b=4&c=2&fr=topcategory_c2",code="gbk",handle=dianshiju)
spider_join()   #等待蜘蛛完成所有爬去任务