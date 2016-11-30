#from newtest.items import DmozItem
#coding:utf-8
import scrapy
import MySQLdb
import MySQLdb.cursors
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')
info_conn=MySQLdb.connect(host='172.16.13.177',user='root',passwd='123456',port=3306,charset='utf8',\
                       db="bx_abc",cursorclass = MySQLdb.cursors.DictCursor)
cur = info_conn.cursor()
com_name=[u"平安人寿",u"太平洋人寿",u"中国人寿",u"新华人寿",u"泰康人寿",u"太平人寿",u"阳光人寿",u"友邦保险",u"人保寿险"\
          ,u"民生人寿",u"富德生命人寿",u"华夏人寿",u"信诚人寿",u"合众人寿",u"百年人寿",u"华泰人寿"\
           ,u"友邦人寿",u"天安人寿",u"中华人寿"]

class XiangrikuiSpider(scrapy.Spider):
    name = "XiangrikuiSpider"
    allowed_domains = ["188bx.com"]
    start_urls=[]
    for i in range(1,97):
        start_urls.append("http://www.188bx.com/service/PageQuest.ashx?pageSize=20&pageIndex="+str(i))
    def parse(self, response):
        urls=[]
        for sel in response.xpath('//div[@class="quest_list"]'):
            if int(sel.xpath('div[@class="quest_answer"]/span/text()').extract()[0]) > 0:
                des_url="http://www.188bx.com/"+sel.xpath('div[@class="quest_answer_center"]/div[@class="quest_title"]/a/@href').extract()[0]
                urls.append(des_url)
        for url in urls:
            try:
                cur.execute("select askid from bx_ask_caiji where mark='%s' limit 1" %(url))
                sql_data=cur.fetchone()
            except Exception,e:
                print e
            else:
                if not sql_data:
                    yield scrapy.Request(url, callback=self.des_page)
                else:
                    askid=sql_data["askid"]
                    cur.execute("select count(*) as count from bx_answer_caiji where askid='%s'  " %(askid))
                    sql_data=cur.fetchone()
                    count=sql_data["count"]
                    if count>0:
                        pass
                    else:
                        yield scrapy.Request(url, callback=self.des_page)
    def des_page(self,response):
        item,tmp_ans,tmp={},[],[]
        url=response.url
        ques=response.xpath('//div[@class="qu_answer_top_title"]/text()').extract()[0]
        ques=''.join(re.findall(u'[\u2E80-\u9FFF\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300ba-zA-Z0-9]+',ques))
        for sel in response.xpath('//div[@class="qu_answer_middle"]/div[@class="qu_answer_content"]/div[@class="qu_answer_content_right"]'):
            ans_info=sel.xpath('div[@class="qu_answer_content_top"]/text()').extract()[1]
            ans_com=''.join(re.findall(u'[\u2E80-\u9FFFa-zA-Z0-9]+',ans_info.split('　')[-1])).replace('保险','人寿')
            if ans_com in com_name:
                ans=sel.xpath('div[@class="qu_answer_content_right_msg"]/text()').extract()[0]
                ans=''.join(re.findall(u'[\u2E80-\u9FFF\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\uff01\u300ba-zA-Z0-9]+',ans))
                if not ans in tmp:
                    tmp.append(ans)
                    tmp_ans.append({"ans_com":ans_com,"ans":ans})
            else:
                print ans_com
        if tmp_ans:
            try:
                cur.execute("insert  into bx_ask_caiji values(NULL,'','%s', '%s',0)" %(ques,url))
                print url
            except Exception,e:
                print e
                if "Duplicate entry" in str(e):
                    cur.execute("select askid from bx_ask_caiji where mark='%s' limit 1" %(url))
                    sql_data=cur.fetchone()
                    askid=sql_data["askid"]
                    cur.execute("select count(*) as count from bx_answer_caiji where askid='%s'  " %(askid))
                    sql_data=cur.fetchone()
                    count=sql_data["count"]
                    if count>0:
                        pass
                    else:
                        for i in tmp_ans:
                            try:
                                cur.execute("insert  into bx_answer_caiji values(NULL,'%s','%s', '%s','%s',0)" %(askid,i["ans"],url,i["ans_com"]))
                            except Exception,e:
                                #print e
                                pass
                            finally:
                                info_conn.commit()
                pass
            else:
                    askid =info_conn.insert_id()
                    info_conn.commit()
                    for i in tmp_ans:
                        try:
                            cur.execute("insert  into bx_answer_caiji values(NULL,'%s','%s', '%s','%s',0)" %(askid,i["ans"],url,i["ans_com"]))
                        except Exception,e:
                            print e
                            pass
                        finally:
                            info_conn.commit()