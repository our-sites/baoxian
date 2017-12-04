#coding:utf-8
# write  by  zhou

import  pyquery

def img_handle(html):
    if not html:
        return ''
    a = "<div>" + html + "</div>"
    doc = pyquery.PyQuery(a)
    for i in doc("img"):
        src = pyquery.PyQuery(i).attr("src")
        if src and src.startswith("/media/"):
            pyquery.PyQuery(i).attr("src","https://upyun.bao361.cn" + src)
    return doc.html()

print img_handle("<div><img  src='/media/aa' ><img src='/aa/bb/cc'></div>")
print img_handle("xxxx")
print img_handle("<img  src='/media/aa' >aaaa<img src='/aa/bb/cc'>")
print img_handle(("<img a='11'>"))
print img_handle("")
print img_handle("1")