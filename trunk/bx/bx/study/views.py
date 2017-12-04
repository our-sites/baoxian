#coding:utf-8
# write  by  zhou
from django.http import  HttpResponse
from django.views.decorators.csrf import  csrf_exempt
from  ..models import  StudyVideo
import time
import  traceback
import json
from django.shortcuts import  render_to_response
from django.template.context import  RequestContext
from django.core.paginator import Paginator
import re
import  urllib
from django.db.models import Q
from django.conf import  settings
JsonResponse=lambda x:HttpResponse(json.dumps(x),mimetype="application/javascript")


@csrf_exempt
def add_youkuvideo(request):
    post_info=request.POST
    try:
        video_type=post_info.get("video_type")
        video_type=int(video_type)
        assert  video_type in (1,2,3)
        title=post_info.get("title")
        assert  title
        video_id=post_info.get("video_id")
        video_imgurl=post_info.get("video_imgurl")
        assert  video_imgurl.startswith("http://") or video_imgurl.startswith("https://") \
           or  video_imgurl.startswith("/")
        assert  video_id
        author=post_info.get("author")
        assert author
        duration=post_info.get("duration")
        duration=int(duration)
        author_imgurl=post_info.get("author_imgurl")
        assert  author_imgurl.startswith("http://") or author_imgurl.startswith("https://")\
                or author_imgurl.startswith("/")
        video=StudyVideo(video_type=video_type,video_source=1,title=title,
                         video_id=video_id,author=author,author_imgurl=author_imgurl,
                         duration=duration,video_imgurl=video_imgurl
                         )
        video.save()
        return  JsonResponse({"status":True,"message":"success","vid":video.vid})
    except Exception as e :
        return  JsonResponse({"status":False,"message":str(e)})

