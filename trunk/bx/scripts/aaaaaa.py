#coding:utf-8
import re
import urllib2
import  json
import  requests

debug_host="http://0.0.0.0:8000"
formal_host="https://app.bao361.cn"

host=formal_host
# session_key_data=requests.get(host+"/app/get_session_key")
# print session_key_data.text,json.loads(session_key_data.text)
# raise
session_key="0fKHHd1jrAqodHIZvwWRNB+/lP19ZLyBJIHhdkLlhvg="
result=requests.post(url=host+"/app/api_gateway/?method=bx.app.views.login.login",
                    data={"phone":"18749679769",
                            "password":"gc7232275"},
                    headers={"Session":session_key})
print result.text

result=requests.post(url=host+ "/app/api_gateway/?method=bx.app.views.study.video_detail",
                    data={"vid":37
                          },
                    headers={"Session":session_key})
print result.text

result=requests.post(url=host+ "/app/api_gateway/?method=bx.app.views.study.video_comment_list",
                    data={"vid":37,
                          "num":"10"
                          },
                    headers={"Session":session_key})
print result.text


