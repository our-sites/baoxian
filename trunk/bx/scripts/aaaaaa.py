#coding:utf-8
import re
import urllib2
import  json
import  requests
import  base64

debug_host="http://0.0.0.0:8000"
formal_host="https://app.bao361.cn"

host=debug_host
# session_key_data=requests.get(host+"/app/get_session_key")
# print session_key_data.text,json.loads(session_key_data.text)
# raise
session_key="0fKHHd1jrAqodHIZvwWRNB+/lP19ZLyBJIHhdkLlhvg="
result=requests.post(url=host+"/app/api_gateway/?method=bx.app.views.login.login",
                    data={"phone":"18749679769",
                            "password":"gc7232275"},
                    headers={"Session":session_key})
print result.text

data = open("baidu.png","rb").read()
data = base64.b64encode(data)

result=requests.post(url=host+ "/app/api_gateway/?method=bx.app.views.my.my_photo_add",
                    data={"img_name":"xx.png",
                          "img_b64_data":data},
                    headers={"Session":session_key})
print result.text


raise
result=requests.post(url=host+ "/app/api_gateway/?method=bx.app.views.homepage.index",
                    data={"uid":1753
                          },
                    headers={"Session":session_key})
print result.text
