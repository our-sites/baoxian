#coding:utf-8
# write  by  zhoufrom gcutils.encrypt import md5
from django.http import HttpResponseRedirect
import urllib
import time
import datetime
import random
from ...models import Area,StudyVideo,StudyVideoComment
from django.views.decorators.csrf import csrf_exempt
from ...myauth.models import MyUser
JsonResponse=lambda x:HttpResponse(json.dumps(x),mimetype="application/javascript")
from bx.utils.aes import *
from bx.decorators import *
from bx.utils.sms import *


@app_api(login_required=True)
def video_list(request):
    '''
    功能说明:
    课堂--获取视频列表,排序方式vid从大到小, vid越大表明该视频的距离当前时间越短,该视频越新.
    参数说明:
    max_vid  vid的最大值,int,    通过控制此项可以实现加载更多的效果.    非必填项
    type       类型, 取值 0  或 1  2  3  0代表全部   1代表已经新手   2代表签单 3代表增员
    num    数量 ,范围0-15,必填项
    返回数据说明:
    当传递的参数为:
    num:2 时,返回的数据如下:
    {
     "errorCode": 0,
     "formError": {},
     "message": "",
     "data": [
      {
       "vid": 37,   视频ID
       "author": "ababy5262", 视频作者
       "addtime": 1508293791,   视频添加时间
       "good_num": 0,   被赞的次数
       "title": "\u7f8e\u56fd\u53cb\u90a6\u4fdd\u9669\u65e0\u9521\u670d\u52a1\u90e8\u589e\u5458\u7bc713003325262", 视频标题
       "play_num": 0,   被播放的次数
       "duration": 34,  时长(秒)
       "author_imgurl": "https://www.bao361.cn/media/img/41/967aa7a6f52ed9ac6c03bf86b159bb25.jpg", 作者头像url
       "video_imgurl": "https://www.bao361.cn/media/img/29/0a894cddafaf0ccef40f45749feff70d.jpg"   视频预览图url
      },
      {
       "vid": 36,
       "author": "\u817e\u8baf\u7528\u62371463707750989160",
       "addtime": 1508293748,
       "good_num": 0,
       "title": "\u4fdd\u9669\u94f6\u4fdd\u7cbe\u82f1\u5206\u4eab\u8bb2\u597d\u4eba\u529b\u4e09\u8bb2\u589e\u5458\u9762\u8c08\u4e0d\u518d\u96be",
       "play_num": 0,
       "duration": 960,
       "author_imgurl": "https://www.bao361.cn/media/img/2/d037cd215f08a48d8e4f5283195d3792.jpg",
       "video_imgurl": "https://www.bao361.cn/media/img/77/d7875f1d88e4dbb5fd6ef3595bf96b9d.jpg"
      }
     ]
    }
    '''
    params={}
    post_info=request.POST
    max_vid=post_info.get("max_vid")
    _type=post_info.get("type")
    num=post_info.get("num")
    try:
        assert num
        num=int(num)
        assert num<=15 and num>0
    except:
        raise FieldError("num","num不合法!num应该0-15范围内")
    if max_vid:
        try:
            max_vid=int(max_vid)
        except:
            raise FieldError("max_vid","max_vid 必须是一个整数")
        params["vid__lt"]=int(max_vid)
    if _type:
        assert _type in ("0","1","2","3"),FieldError("type","type取值为 0 或 1  或 2  或 3")
        if _type == "0":
            pass
        else:
            params["video_type"] = int(_type)
    study_list=StudyVideo.objects.filter(**params).order_by("-vid")[:num].values(
                                    "vid","title","addtime",
                                    "video_imgurl",
                                    "author","author_imgurl",
                                    "duration","good_num","play_num")
    result=[]
    for i in study_list:
        result.append(i)
    return  result



@app_api(login_required=True)
def video_detail(request):
    '''
    功能说明:
    课堂-获取一个视频的详细信息(视频播放页的flash播放器的引用可以参考 https://www.bao361.cn/static/testsegement.html)
    参数说明:
    vid     视频id, 必传
    返回数据:
        {
     "errorCode": 0,
     "formError": {},
     "message": "",
     "data": {
      "vid": 16,
      "author": "\u7f51\u7edc\u8425\u9500\u5165\u95e8",  作者
      "addtime": 1508290175, 添加时间
      "good_num": 0,  #被赞次数
      "video_id": "XMjc0ODAwODgyMA==", #视频播放ID, 主要是加载flash播放器时候用.
      "play_num": 1, #播放次数
      "duration": 370, #时长(秒)
      "author_imgurl": "https://www.bao361.cn/media/img/3/4dbd4d92062221d8cd68d2b015dc6adf.png", 作者url
      "video_imgurl": "https://www.bao361.cn/media/img/16/7f18c502012a645879ded2694665063c.jpg", 视频缩略图url
      "title": "\u9500\u552e\u6280\u5de7\u8bdd\u672f (7)"   #视频标题,
      "comment_num":11,"被评论次数"
     }
    }
    '''
    post_info=request.POST
    vid=post_info.get("vid")
    video_object=StudyVideo.objects.get(vid=int(vid))
    video_object.play_num+=1
    video_object.save()
    result={}
    for i in   ( "vid","title","addtime",
                                    "video_imgurl","video_id",
                                    "author","author_imgurl",
                                    "duration","good_num","play_num","comment_num"):
        result[i]=getattr(video_object,i)

    return result





@app_api(login_required=True)
def video_good(request):
    '''
    功能说明：
    对某个视频点赞
    参数说明：
    vid 必填，视频的vid，
    返回值说明：
    {"errorCode":0,"formError":{},"data":1,"message":""}   #data的值代表 点过赞之后,该视频一共被赞的次数.
    '''
    post_info=request.POST
    vid=post_info.get("vid")
    vid_object=StudyVideo.objects.get(vid=int(vid))
    #comment_object=StudyVideoComment.objects.get(id=int(id))
    #comment_object.good_num+=1
    #comment_object.save()
    vid_object.good_num+=1
    vid_object.save()
    return  vid_object.good_num



@app_api(login_required=True)
def video_comment_list(request):
    '''
    功能说明:
    获取视频的评论,排序方式id从大到小, id越大表明该评论的距离当前时间越短,该评论越新.
    参数说明:
    vid  视频的vid,必传
    max_id  id的最大值,int,    通过控制此项可以实现加载更多的效果.    非必填项
    num    数量 ,范围0-15,必填项
    返回数据说明：
      {
     "errorCode": 0,
     "formError": {},
     "message": "",
     "data": {
      "rows": 列表数据
      [
      {
       "id": 222, 该条评论的ID
      "uid": 16,  发表评论的用户的ID
      "name": "\u7f51\u7edc\u8425\u9500\u5165\u95e8",  发表评论的用户的用户名
      "addtime": 1508290175, 添加时间
      "good_num": 0,  #被赞次数
      "imgurl": "https://www.bao361.cn/media/img/3/4dbd4d92062221d8cd68d2b015dc6adf.png", 发表评论的用户头像URL
      "content": "\u9500\u552e\u6280\u5de7\u8bdd\u672f (7)"   #评论内容
     }
     ],
     "total":111   该vid的所有评论总数
     }
    }
    '''
    params={}
    post_info=request.POST
    vid=post_info.get("vid")
    vid=int(vid)
    params["vid"]=vid
    max_id=post_info.get("max_id")
    num=post_info.get("num")
    try:
        assert num
        num=int(num)
        assert num<=15 and num>0
    except:
        raise FieldError("num","num不合法!num应该0-15范围内")
    if max_id:
        try:
            max_id=int(max_id)
        except:
            raise FieldError("max_id","max_id 必须是一个整数")
        params["id__lt"]=int(max_id)

    comment_list=StudyVideoComment.objects.filter(**params).order_by("-id")[:num]
    uid_list=list(set(i.uid for i in comment_list))
    user_list=MyUser.objects.filter(uid__in=uid_list)
    uid_dict=dict([(i.uid,i) for i in user_list])
    vid_object=StudyVideo.objects.get(vid=vid)
    result=[]
    for i in comment_list:
        user=uid_dict[i.uid]
        _={}
        _["uid"]=user.uid
        _["name"]=user.get_hide_namecontent()
        _["img_url"]=user.get_img_url()
        _["addtime"]=i.addtime
        _["content"]=i.content
        _["good_num"]=i.good_num
        _["id"]=i.id
        result.append(_)
    return  {"rows":result,"total":vid_object.comment_num}

@app_api(login_required=True)
def video_comment_add(request):
    '''
    功能说明：
    添加评论
    参数说明：
    vid 评论的视频的vid ,必填项
    content 评论的内容 ，必填项
    返回值说明：
    添加成功：
    {"errorCode":0,"formError":{},"data":true,"message":""}
    '''
    post_info=request.POST
    vid=post_info.get("vid")
    content=post_info.get("content")
    video_object=StudyVideo.objects.get(vid=int(vid))
    video_object.add_comment(request.myuser,content)
    return True


@app_api(login_required=True)
def video_comment_goodcom(request):
    '''
    功能说明：
    对某个评论点赞
    参数说明：
    id 必填，评论的ID，
    返回值说明：
    {"errorCode":0,"formError":{},"data":1,"message":""}   #data的值代表 点过赞之后,该评论一共被赞的次数.
    '''
    post_info=request.POST
    id=post_info.get("id")
    comment_object=StudyVideoComment.objects.get(id=int(id))
    comment_object.good_num+=1
    comment_object.save()
    return  comment_object.good_num



