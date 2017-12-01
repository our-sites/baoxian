#coding:utf-8

from urlparse import urljoin
from urlparse import urlparse
from urlparse import urlunparse
from posixpath import normpath
from threadspider.utils.db import   MySQLMgr
from snownlp import SnowNLP
import jieba.posseg as pseg
import json
import requests
from pyquery import  PyQuery
import  urllib
import  urllib2
import  traceback
import  HTMLParser
import  re
import  sys
import  time
import  random
reload(sys)
sys.setdefaultencoding("utf-8")


def filter_tags(htmlstr):
    s=re.sub("<[^<>]+>",'',htmlstr)
    return s

def replace_charentity(htmlstr):
    htmlstr=htmlstr.replace("&quot;",'"')
    htmlstr=htmlstr.replace("&amp;",'&')
    htmlstr=htmlstr.replace("&lt;",'<')
    htmlstr=htmlstr.replace("&gt;",'>')
    htmlstr=htmlstr.replace("&nbsp;",' ')
    return htmlstr

def get_simple_content(self) :
    a = filter_tags(self)
    b = replace_charentity(a)
    _ = HTMLParser.HTMLParser()
    return _.unescape(b.strip())

'''
word_len:文本长度
zhaiyao:摘要信息
titile:标题
kw:关键词
before_context:处理前的文本
later_context:经过翻译之后拼接后的文本
data:{"src":要翻译的词,"tgt:翻译之后转换的结果}
'''
class Word_analyse(object):
    '''
    dict_content 形式{title:xxxx ,context:xxx}

    '''
    def __init__(self,dict_content):
        if isinstance(dict_content,dict):
            self.title = dict_content.get('title')
            self.context = dict_content.get('context')
        else:
            self.title = ''
            self.context = ''
    def get_result(self):
        kw = []
        if self.context:
            summary = SnowNLP(self.context).summary()
            words = pseg.cut(self.context)
            for word,flag in words:
                # print word,flag
                if flag== 'v':
                    pass
                else:
                    kw.append(word)
            if not isinstance(self.context,unicode):
                self.context  = unicode(self.context,'utf-8')
            #是否对特殊字符进行处理？
            # for i  in ' n!"#$%&()*+,-./:;<=>?@[\]^_`{|}~':
            #     self.context.replace('', i)
            #content = self.context.encode('gbk').decode('gbk')
            content=self.context
            word_len = len(content)
        else:
            content = ''
            summary = ''
            word_len = 0
        if  content:

            cut_words = content[int(round(word_len * 0.9)):]
            #print "截取后的词",cut_words
            try:
                #中文转韩文zh_to_kor
                data = requests.post("http://fanyi.baidu.com/v2transapi",data={"from": "zh", "to": "kor",
                                                                                     "query": cut_words, "transtype": "translang",
                                                                                 "simple_means_flag": "3"},timeout=10)
                response = data.text
                translate_result_kor = json.loads(response).get("trans_result").get("data")[0].get("dst")
                if translate_result_kor:
                    # 韩文转化为中文kor_to_zh
                    data = requests.post("http://fanyi.baidu.com/v2transapi", data={"from": "kor", "to": "zh",
                                                                            "query": translate_result_kor,
                                                                            "transtype": "translang",
                                                                            "simple_means_flag": "3"})
                    response = data.text
                    translate_result = json.loads(response).get("trans_result").get("data")[0].get("dst")
                else:
                    translate_result = ''
            except Exception as  e:
                translate_result = ''
                print str(e)
            if translate_result:
                #对翻译后对文章进行拼接
                join_context=content[:int(round(word_len * 0.9))]+translate_result
            else:
                join_context=content
        else:
            join_context,cut_words,translate_result=content,'',''
        return {'title':self.title,'kw':set(kw),'zhaiyao':summary,'later_context':join_context,'before_context':self.context,'word_len':word_len,"data":[{'src':cut_words,"tgt":translate_result}]}

def myjoin(base, url):
    url1 = urljoin(base, url)
    arr = urlparse(url1)
    path = normpath(arr[2])
    return urlunparse((arr.scheme, arr.netloc, path, arr.params, arr.query, arr.fragment))

def save_img(content,extname):
    img_content=content
    a=urllib2.urlopen("https://www.bao361.cn/api/upload_img",data=urllib.urlencode({"extname":extname,"file":img_content}) ).read()
    return  json.loads(a)["imgurl"]


mgr=MySQLMgr("118.89.220.36",3306,"bx_abc","bx_user","gc895316")



result=mgr.runQuery('''select zid,title,content,`from`  from bx_consult WHERE status=0   limit 10''',())

for _zid,title,content,_from  in  result:
    if not content:
        mgr.runOperation('''delete from  bx_consult   where zid=%s''',
                         (_zid,))
    else:
        doc=PyQuery("<div>"+ content+"</div>")
        for j in doc("img"):
            src=PyQuery(j).attr("src")
            if _from.startswith("http://") or _from.startswith("https://"):
                try:
                    _url=myjoin(_from,src)
                    print _url
                    request=urllib2.Request(_url)
                    request.headers["Upgrade-Insecure-Requests"]=1
                    request.headers["User-Agent"]="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36 QQBrowser/4.2.4718.400"
                    request.headers["Accept"]="text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
                    _imgdata=urllib2.urlopen(request,timeout=3).read()
                    extname="."+ _url.split(".")[-1]
                    if "/" in extname:
                        extname=".jpg"
                    new_name=save_img(_imgdata,extname)
                    print new_name
                except Exception as e :
                    traceback.print_exc()
                else:
                    pass
                    j.set("src",new_name)
        simple_content=get_simple_content(content)
        if len(simple_content)>20:
            zhaiyao= ",".join(SnowNLP(simple_content).summary(5))
        else:
            zhaiyao=simple_content
        keywords=" ".join ([i  for i,j in   pseg.cut(title) if j!="v"][:5])
        print keywords
        print zhaiyao
        # for _ in  doc("p"):
        #     if PyQuery(_).children().__len__()==0:
        #         _text=PyQuery(_).text()
        #         if len(_text)>10:
        #             test = Word_analyse({"title": "", "context": _text})
        #             result = test.get_result()
        #             PyQuery(_).html(result["later_context"])
        doc("script").remove()
        content= doc.html()
        mgr.runOperation('''update bx_consult  set content=%s,status=3,keywords=%s ,abstract=%s where zid=%s''',(content,keywords,zhaiyao,_zid))
        print _zid

