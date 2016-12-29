#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/24.
# ---------------------------------
import ahocorasick
import  sys
import  re
def _filter_tags(htmlstr):
    s=re.sub("<[^<>]+>",'',htmlstr)
    return s
def _replace_charentity(htmlstr):
    htmlstr=htmlstr.replace("&quot;",'"')
    htmlstr=htmlstr.replace("&amp;",'&')
    htmlstr=htmlstr.replace("&lt;",'<')
    htmlstr=htmlstr.replace("&gt;",'>')
    htmlstr=htmlstr.replace("&nbsp;",' ')
    return htmlstr
ac_obj=ahocorasick.AhoCorasick(*[i.decode("utf-8") for i in sys.argv[1:]])
for i in sys.stdin:
    i=i.strip()
    info=i.split("\t")
    try:
        info=[j.decode("utf-8") for j in info ]
        info[-1]=_filter_tags(_replace_charentity(info[-1]))
        rowkey,prodesc=tuple(info)
    except:
        pass
    else:
        result=ac_obj.search(prodesc)
        if len(result)==0:
            pass
        else:
            print (rowkey+"\t"+"|".join(result)).encode("utf-8")
