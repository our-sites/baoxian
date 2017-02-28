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

def get_simple_content(self):
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
    windows_size 有三种类型high,center,low,分别代表上中下或者33%，%33-%66，%66-%100
    '''
    def __init__(self,dict_content,windows_size=None):
        if isinstance(dict_content,dict):
            self.title = dict_content.get('title')
            self.context = dict_content.get('context')
        else:
            self.title = ''
            self.context = ''
        self.windows_size = windows_size
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
        if self.windows_size and content:
            if self.windows_size == "high":
                cut_words = content[:int(round(word_len*0.33))]
            elif self.windows_size == 'center':
                cut_words = content[int(round(word_len*0.33)):int(round(word_len * 0.33)*2)]
            elif self.windows_size == 'low':
                cut_words = content[int(round(word_len * 0.33*2)):]
            #print "截取后的词",cut_words
            try:
                #中文转韩文zh_to_kor
                data = requests.post("http://fanyi.baidu.com/v2transapi",data={"from": "zh", "to": "kor",
                                                                                     "query": cut_words, "transtype": "translang",
                                                                                 "simple_means_flag": "3"},timeout=10)
                response = data.text
                translate_result = json.loads(response).get("trans_result").get("data")[0].get("dst")
                if translate_result:
                    # 韩文转化为中文kor_to_zh
                    data = requests.post("http://fanyi.baidu.com/v2transapi", data={"from": "kor", "to": "zh",
                                                                            "query": translate_result,
                                                                            "transtype": "translang",
                                                                            "simple_means_flag": "3"})
                    response = data.text
                    translate_result = json.loads(response).get("trans_result").get("data")[0].get("dst")
                else:
                    translate_result = '未请求到数据'
            except Exception as  e:
                translate_result = e
            #对翻译后对文章进行拼接
            try:
                if self.windows_size == "high":
                    join_context = content.replace(content[:int(round(word_len*0.33))],translate_result)
                elif self.windows_size == "center":
                    join_context = content.replace(content[int(round(word_len*0.33)):int(round(word_len * 0.33)*2)], translate_result)
                elif self.windows_size == "low":
                    join_context = content.replace(content[int(round(word_len * 0.33*2)):], translate_result)
                else:
                    join_context=content
            except:
                join_context=content
        else:
            join_context,cut_words,translate_result='','',''
        return {'title':self.title,'kw':set(kw),'zhaiyao':summary,'later_context':join_context,'before_context':self.context,'word_len':word_len,"data":[{'src':cut_words,"tgt":translate_result}]}

def myjoin(base, url):
    url1 = urljoin(base, url)
    arr = urlparse(url1)
    path = normpath(arr[2])
    return urlunparse((arr.scheme, arr.netloc, path, arr.params, arr.query, arr.fragment))

def save_img(content,extname):
    img_content=content
    a=urllib2.urlopen("http://img.baoxiangj.com/api/upload_img",data=urllib.urlencode({"extname":extname,"file":img_content}) ).read()
    return  json.loads(a)["imgurl"]


mgr=MySQLMgr("118.89.220.36",3306,"bx_abc","bx_user","gc895316")

#result=[]
_id=21773
while 1:
    result=mgr.runQuery('''select zid,title,content,`from`  from bx_consult WHERE status=1 and zid>%s  limit 50''',(_id,))
    #result+=_
    _id=max([i[0] for i in result])
    for _zid,title,content,_from  in  result:
        if not content:
            mgr.runOperation('''update bx_consult  set status=0 where zid=%s''',
                             (_zid,))
        else:
            doc=PyQuery("<div>"+ content+"</div>")
            for j in doc("img"):
                src=PyQuery(j).attr("src")
                if _from.startswith("http://") or _from.startswith("https://"):
                    try:
                        _url=myjoin(_from,src)
                        _imgdata=urllib.urlopen(_url).read()
                        extname="."+ _url.split(".")[-1]
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
            for _ in  doc("p"):
                if PyQuery(_).children().__len__()==0:
                    _text=PyQuery(_).text()
                    if len(_text)>10:
                        test = Word_analyse({"title": "", "context": _text}, windows_size='center')
                        result = test.get_result()
                        PyQuery(_).html(result["later_context"])

            content= doc.html()
            mgr.runOperation('''update bx_consult  set content=%s,status=1,keywords=%s ,abstract=%s where zid=%s''',(content,keywords,zhaiyao,_zid))
            print _zid
            if len(result) < 50:
                break