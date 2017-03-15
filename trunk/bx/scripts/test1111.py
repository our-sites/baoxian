#coding:utf8
__author__ = 'chenhuachao'

from snownlp import SnowNLP
import jieba.posseg as pseg
import json
import requests
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
            content = self.context.encode('gbk').decode('gbk')
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
                                                                                 "simple_means_flag": "3"})
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
            if self.windows_size == "high":
                join_context = content.replace(content[:int(round(word_len*0.33))],translate_result)
            elif self.windows_size == "center":
                join_context = content.replace(content[int(round(word_len*0.33)):int(round(word_len * 0.33)*2)], translate_result)
            elif self.windows_size == "low":
                join_context = content.replace(content[int(round(word_len * 0.33*2)):], translate_result)
        else:
            join_context,cut_words,translate_result='','',''
        return {'title':self.title,'kw':set(kw),'zhaiyao':summary,'later_context':join_context,'before_context':self.context,'word_len':word_len,"data":[{'src':cut_words,"tgt":translate_result}]}


if __name__=="__main__":
    test = Word_analyse({"title":u"我是中国人","context":u"很高兴能够来参加一年一度的财新峰会，确实是个思想的盛宴。今天我讲的就是本次论坛的主题“金融创新与监管”。我认为，金融创新与监管永远是一对矛盾，需要加以平衡。一方面，创新能够带来金融市场的繁荣，也可能带来风险;另一方面，如果强化金融监管，出台管制措施，又可能对金融市场产生一定的抑制作用，使其失去活力。比如，最近有媒体报道在特朗普当选美国总统后，将在强化金融监管方面有所动作，欧洲的金融业高管们听到这个消息后很振奋，觉得好机会来了。因此，我认为金融创新与监管需要认真加以平衡。"},windows_size='center')
    result = test.get_result()
    print result["zhaiyao"][0]
    #print result.get('data')[0].get('tgt')
    print result.get('before_context')
    print result.get('later_context')
