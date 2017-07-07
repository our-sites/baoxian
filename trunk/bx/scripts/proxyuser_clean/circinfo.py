#!/usr/bin/env python
#coding=utf-8

from vcode_distinguish import login,urlretrieve,remove_line,two_valued,pic_cut,getverticode
import requests
import time
from lxml import etree
from bs4 import BeautifulSoup

def get_data_post(headers,code,**kwargs):
    evelop_code=kwargs.get('evelop_code','')
    certificate_code=kwargs.get('certificate_code','')
    name=kwargs.get('name','')
    if code and evelop_code :
        data={'evelop_code':evelop_code,'valCode':code,'certificate_code':'','name':''}
    elif code and certificate_code :
        data={'evelop_code':'','valCode':code,'certificate_code':certificate_code,'name':''}
    elif code and name :
        data={'evelop_code':'','valCode':code,'certificate_code':'','name':name}
    else :
        return {"status":False}
    url="http://iir.circ.gov.cn/web/validateCodeAction!ValidateCode.html?validateCode=%s&dateTime=%s"%(code,str(int(time.time() * 1000)))
    print url,headers
    D = requests.post(url, headers=headers)
    try :
        DATA = requests.post('http://iir.circ.gov.cn/web/baoxyx!searchInfoBaoxyx.html',headers=headers,data=data)
    except Exception,e:
        print e
        time.sleep(30)
        return kwargs
    html = DATA.content
    soup = BeautifulSoup(html, 'lxml')
    selector = etree.HTML(html)
    if not name :
        KEYS = selector.xpath('//table/tr/th')[:-1]
        Value = selector.xpath('//table/tr/td')[4:-1]
        for index,K in enumerate(KEYS):
            print K.text,':',Value[index].text
            kwargs[''.join(K.text.split())]=Value[index].text.replace(' ', '') if Value[index].text else ''
    else :
        #evelop_code_list=selector.xpath('//table/tbody/tr/td[not @width]')
        evelop_code_list=selector.xpath('//table/tbody/tr/td')
        for e in evelop_code_list :
            print e
        print name,'~~~~~',data,evelop_code_list,selector.text
    return kwargs
def data_handle(evelop_code):
  user_agent_list=["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0","Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E)","Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729)","Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)","Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)"]
  while True :
    T = str(int(time.time() * 1000))
    url = 'http://iir.circ.gov.cn/web/servlet/ValidateCode?time=' + T
    user_agent = user_agent_list[int(T)%5]
    #headers = {'user-agent': user_agent , 'Referer': "http://iir.circ.gov.cn/web/" , 'Cookie':"UM_distinctid=15c1426cc7e92-0c5498fea-19754660-1fa400-15c1426cc7f402; _gscu_1407742603=949866994n1dyn68; Hm_lvt_6a2f36cc16bd9d0b01b10c2961b8900c="+str(int(T[:-3])-86400)+"; bjh-20480-%3FVRF-CX%3FGroup_ZJY_YW=BOABGEAKHICD; JSESSIONID=00008ZkZELNxu9e0fonXym0JfHe:148amfs12; CNZZDATA1619462=cnzz_eid%3D220465032-"+str(int(T[:-3])-17506)+"-http%253A%252F%252Fwww.circ.gov.cn%252F%26ntime%3D"+str(int(T[:-3])-2400)}
    headers = {'user-agent': user_agent , 'Referer': "http://iir.circ.gov.cn/web/" , 'Cookie':"JSESSIONID=00007jbvF15LP2aG0VfRxaVA55o:14jjldep8; bjh-20480-%3FVRF-CX%3FGroup_ZJY_YW=BGABGEAKHJCD; UM_distinctid=15c3d815b600-006c30d3a-19754660-1fa400-15c3d815b623c7; CNZZDATA1619462=cnzz_eid%3D1386428383-1495678811-%26ntime%3D1495678811"}
    result = requests.get(url, headers=headers)
    with open('tmp_abc.bmp', 'wb')as f:
        f.write(result.content)
    f.close()
    urlretrieve('tmp_abc.bmp', 'captcha.gif')
    remove_line('captcha.gif','./','./')
    two_valued('captcha.gif','./','./')
    pic_cut('captcha.gif','./','./word/',0)

    code = getverticode()
    code = code[2:]+code[:2]
    if len(code) == 4 and code.isdigit() :
        print "Vcode Distinguish OK!!!"
        break
  try :
      D = get_data_post(headers,code,evelop_code=evelop_code)
  except :
      return {}
  #print T,D[u'性别']
  return D

if __name__ == '__main__':
    evelop_code='02000045010080002014021019'
    data_handle(evelop_code)

