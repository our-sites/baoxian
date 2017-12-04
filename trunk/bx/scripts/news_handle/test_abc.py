#coding:utf-8
# write  by  zhou


from threadspider.utils.db import  MySQLMgr
import  pyquery
#mgr=MySQLMgr("127.0.0.1",3306,"bx_abc","root","123456")
#result=mgr.runQuery("select content from bx_news limit 100")
a='''        <img alt="涨姿势：交了这么多年的公积金到底有什么用？怎么用？" img_height="426" img_width="640" inline="0" src="/media/img/36/03723ce9f4ac370034334269cfed4fd0.jpg"/></p><p>&#13;'''
_=pyquery.PyQuery("<div>"+a+"</div>")
print [  pyquery.PyQuery(i).attr("src")  for i in   _("img[src^='/media/']")]