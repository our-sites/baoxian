#coding:utf-8
# write  by  zhou


from django.http import  HttpResponse,HttpResponseNotFound,Http404
from django.views.decorators.csrf import  csrf_exempt
from  ..models import  News,NewsCate
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

from ..views import mobile_browser_adaptor_by_host

@mobile_browser_adaptor_by_host(settings.M_HOST_FUN,{"news_index.html":"m_news_index.html"})
def index(request,tag=None,cateid=None):
    path=request.path
    page=re.search(r"/(\d+)\.html",path)
    cateobj=None
    if ".html" not in request.path:
        non_page_url=request.path
    else:
        non_page_url="/".join(request.path.split("/")[:-1])+"/"
    if page:
        page=int(page.groups()[0])
    else:
        page=1
    cate1_list=NewsCate.objects.filter(level=1)
    print tag,cateid,page
    if tag:
        tag=urllib.unquote(tag.strip("/"))
        news=News.objects.extra(where=["FIND_IN_SET('%s',tags)"%tag])


    elif cateid!=None:
        cateid=int(cateid)
        cateobj=NewsCate.objects.get(cateid=cateid)
        news=News.objects.filter(Q(cate1=cateid)|Q(cate2=cateid),status=1)
    else:
        news=News.objects.filter(status=1)
    paginator=Paginator(news,9)
    print paginator.num_pages
    print page,type(page)
    info=paginator.page(page)
    return  render_to_response("news_index.html",locals(),context_instance=RequestContext(request))




def  tags(request):
    return  HttpResponse("tags")


@mobile_browser_adaptor_by_host(settings.M_HOST_FUN,{"news_detail.html":"m_news_detail.html"})
def detail(request,nid):
    try:
        info=News.objects.get(nid=int(nid),status=1)
    except  News.DoesNotExist:
        raise Http404
    info.see_num+=1
    info.save()
    get_info=request.GET
    if get_info.has_key("good"):
        info.good_num+=1
        info.save()
        _=json.dumps({"status":True,"message":info.good_num})
        return  HttpResponse(_,mimetype="application/javascript")
    try:
        next_obj=News.objects.filter(nid__gt=nid,status=1).order_by("nid")[0]
    except:
        next_obj=None
    try:
        last_obj=News.objects.filter(nid__lt=nid,status=1).order_by("-zid")[0]
    except:
        last_obj=None
    _infos=News.objects.filter(cate1=info.cate1,status=1).order_by("-addtime")[:16]
    hot_infos=_infos[:8]
    relate_infos=_infos[8:]
    return  render_to_response("news_detail.html",locals(),context_instance=RequestContext(request))


def  cate1_list(request):
    _= NewsCate.objects.filter(level=1)
    data=[(i.cateid,i.catename)  for i in _]
    return HttpResponse(json.dumps(data,ensure_ascii=False,indent=True),mimetype="application/javascript")



def cate2_list(request):
    get_info=request.GET
    cate1=get_info.get("cate1","")
    if cate1:
        cate1=int(cate1)
        _=NewsCate.objects.filter(level=2,parentid=cate1)
    else:
        _=NewsCate.objects.filter(level=2)
    data=[(i.cateid,i.catename)  for i in _]
    return HttpResponse(json.dumps(data,ensure_ascii=False,indent=True),mimetype="application/javascript")

def get_cate_id(request):
    get_info=request.GET
    try:
        catename=get_info.get("catename")
        cate_obj=NewsCate.objects.get(catename=catename,level=2)
    except Exception as e :
        return  HttpResponse(json.dumps({"status":False,"message":str(e)}))
    else:
        return  HttpResponse(json.dumps({"status":True,"message":"success","data":[cate_obj.cateid,cate_obj.parentid]}))

@csrf_exempt
def add_news(request):
    post_info=request.POST
    print post_info.keys()

    try:
        secret=post_info.get("secret")
        assert  secret=="gc7232275","secret error!"
        title=post_info.get("title","")
        assert  title ,"title must not be empty"
        _from= post_info.get("from")
        assert  _from
        assert _from.startswith("http://") or _from.startswith("https://")
        try:
            News.objects.get(_from=_from)
        except:
            pass
        else:
            raise Exception("url has exists!")
        content=post_info.get("content","")
        assert  content,"coutent must not be empty"
        tags=post_info.get("tags","")
        assert  tags,"tags must not be empty"
        keywords=post_info.get("keywords","")
        assert  keywords,"keywords must not be empty"
        description=post_info.get("description","")
        abstract=post_info.get("abstract","")
        assert  abstract,"abstract must not be empty"
        cate1=post_info.get("cate1","")
        cate2=post_info.get("cate2","")
        try:
            cate1=int(cate1)
        except:
            raise Exception("cate1 must be an int")
        try:
            cate2=int(cate2)
        except:
            raise Exception("cate2 must be an int")

        assert NewsCate.objects.filter(cateid=cate1,level=1).count(),"cate1 is not assist"
        assert NewsCate.objects.filter(cateid=cate2,parentid=cate1,level=2).count(),"cate2 is not the children of cate1"
        _=News(title=title,cate1=cate1,cate2=cate2,_from=_from,addtime=int(time.time()),
               content=content,status=1,tags=tags,keywords=keywords,
               description=description,abstract=abstract)
        _.save()
    except Exception as e :
        exception=e
        data={"status":False,"message":exception.message}
        traceback.print_exc()
    else:
        data={"status":True,"message":"Add News  Success!","nid":_.nid}

    return HttpResponse(json.dumps(data),mimetype="application/javascript")

