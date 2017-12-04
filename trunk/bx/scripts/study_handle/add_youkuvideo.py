#coding:utf-8
# write  by  zhou

import  urllib2
import  json
import  urllib
import pyquery
import  sys
reload(sys)
sys.setdefaultencoding("utf-8")

def save_img(content,extname):
    img_content=content
    a=urllib2.urlopen("https://www.bao361.cn/api/upload_img",data=urllib.urlencode({"extname":extname,"file":img_content}) ).read()
    return  "https://www.bao361.cn"+json.loads(a)["imgurl"]

def add_by_youku_videoid(youku_videoid,type):
    '''添加优酷视频到server端
    :param youku_videoid    优酷视频ID
    :param type    视频类型,1 新手    2 签单   3 增员
    '''
    def get_youku_info(youku_videoid):
        youku_videoid=urllib.quote(youku_videoid)
        result=urllib2.urlopen("https://api.youku.com/videos/show.json?\
        client_id=eab6c5f589febec2&video_id=%s"%youku_videoid).read()
        return  json.loads(result)
    info=get_youku_info(youku_videoid)
    user_link=info["user"]["link"]
    user_result=urllib2.urlopen(user_link).read()
    doc=pyquery.PyQuery(user_result)
    user_imgurl=doc("a.user-avatar").children("img").attr("src")
    user_imgurl= save_img(urllib2.urlopen(user_imgurl).read(),"."+user_imgurl.split(".")[-1])
    title=info["title"]
    assert  title
    video_id=youku_videoid
    video_imgurl=info["bigThumbnail"]
    video_imgurl=save_img(urllib2.urlopen(video_imgurl).read(),".jpg")
    duration=int(float(info["duration"]))
    author=info["user"]["name"]
    response_data=urllib2.urlopen("https://www.bao361.cn/study/add_youkuvideo",
                    data=urllib.urlencode({"video_type":str(type),
                                           "title":title,
                                           "video_id":video_id,
                                           "video_imgurl":video_imgurl,
                                           "author":author,
                                           "duration":str(duration),
                                           "author_imgurl":user_imgurl})).read()
    return json.loads(response_data)["status"]


if __name__ == "__main__":
    print   add_by_youku_videoid("XMjc2MTUwOTU1Ng==",1)