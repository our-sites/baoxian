
import  urllib2


def postBaiDu(urls):
    URL = "http://data.zz.baidu.com/urls?site=www.bao361.cn&token=MrHjCbljFlIJxYhk&type=original"
    send_headers = {'Content-Type': 'text/plain'}
    conn = urllib2.Request(URL,urls,send_headers)
    req=urllib2.urlopen(conn,timeout=2)
    return  req.read()