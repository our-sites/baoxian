#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/27.
# ---------------------------------
from django.shortcuts import  render_to_response
from django.http import  HttpResponse,HttpResponseRedirect
from django.template.context import  RequestContext
from myauth.decorators import  login_required
from models import Ask,Company
from models import Consult,Product,Ask,News
import  datetime
from myauth.models import  MyUser
from decorators import  mobile_browser_adaptor_by_host
import  settings
import  json

@mobile_browser_adaptor_by_host(settings.M_HOST_FUN,{"index.html":"m_index.html"})
def home(request):
    #return  HttpResponse(request.myuser.username+request.ip)
    hot_ask=Ask.objects.all().order_by("-ask_time")
    hot_product=Product.objects.all().order_by("-pid")[:8]
    if request.city_id:
        hot_user_proxy=MyUser.objects.filter(is_proxy=1,city_id=request.city_id).order_by("-ans_num","uid")[:16]
        _count=MyUser.objects.filter(is_proxy=1,city_id=request.city_id).count()
        if _count<16:
            hot_user_proxy=MyUser.objects.filter(is_proxy=1,province_id=request.province_id).order_by("-ans_num","uid")[:16]
            if hot_user_proxy.count()<16:
                hot_user_proxy = MyUser.objects.filter(is_proxy=1).order_by("-ans_num", "uid")[:16]

    else:
        hot_user_proxy=MyUser.objects.filter(is_proxy=1).order_by("-ans_num","uid")[:16]

    cids=[i.proxy_cid for i in hot_user_proxy]
    cid_objs=Company.objects.filter(cid__in=cids)
    cid_info=dict([(i.cid,i.shortname) for i in cid_objs])
    for i in hot_user_proxy:
        #if i.proxy_cid:
        i.short_comname=cid_info.get(i.proxy_cid,"")

    # friend_company=Company.objects.all().order_by("-product_weight")
    #hot_zixun_news=Consult.objects.filter(type=4,status=1).order_by("-addtime")[:5]
    #hot_zixun_baike=Consult.objects.filter(type=1,status=1).order_by("-addtime")[:5]
    #hot_zixun_anli=Consult.objects.filter(type=2,status=1).order_by("-addtime")[:5]
    hot_news_1=News.objects.filter(cate1=1).order_by("-nid")[:5]
    hot_news_2=News.objects.filter(cate1=2).order_by("-nid")[:5]
    hot_news_5=News.objects.filter(cate1=5).order_by("-nid")[:5]

    return render_to_response( "index.html",locals(),context_instance=RequestContext(request))


def top_roll_message_api(request):
    message_list=[]
    for i in request.get_allsite_msg:
        message_list.append({"url":i.url,"msg":i.message})
    return  HttpResponse(json.dumps(message_list),mimetype="application/javascript")

def hot_dailiren_api(request):
    if request.city_id:
        user_queryset = MyUser.objects.filter(is_proxy=1,city_id=request.city_id).order_by("-ans_num")[:6]
    else:
        user_queryset= MyUser.objects.filter(is_proxy=1).order_by("-ans_num")[:6]
    data=[]
    for i in user_queryset:
        data.append({"uid":i.uid,"name":i.get_namecontent(),"comname":i.get_short_comname(),
                     "imgurl":i.get_img_url(),"vphone":1 if i.phone else 0,
                     "workyear":i.proxy_workyear})
    return HttpResponse(json.dumps(data),mimetype="application/javascript")

def about(request):
    if request.path=="/about":
        return  HttpResponseRedirect("/about/")
    return render_to_response("about/about.html",locals(),
                              context_instance=RequestContext(request))




def sitemap_index(request):
    def get_zixun_sitemap_lastmod(id):
        id = int(id)
        try:
            info = Consult.objects.filter(zid__gte=id * 10000, zid__lt=(id + 1) * 10000).order_by("-addtime").values("addtime")[0]
            return info["addtime"]
        except:
            return None

    def get_news_sitemap_lastmod(id):
        id = int(id)
        try:
            info = News.objects.filter(nid__gte=id * 10000, nid__lt=(id + 1) * 10000).order_by("-addtime").values("addtime")[0]
            return info["addtime"]
        except:
            return None

    def get_product_sitemap_lastmod(id):
        id = int(id)
        try:
            info = Product.objects.filter(pid__gte=id * 10000, pid__lt=(id + 1) * 10000).order_by("-addtime").values("addtime")[0]
            return info["addtime"]
        except:
            return None

    def get_ask_sitemap_lastmod(id):
        id = int(id)
        try:
            info = Ask.objects.filter(askid__gte=id * 10000, askid__lt=(id + 1) * 10000).order_by("-ask_time").values("ask_time")[0]
            return  info["ask_time"]
        except:
            return None

    _=Consult.objects.all().order_by("-zid")[0]
    max_id=_.zid
    zixun_info=[(i,get_zixun_sitemap_lastmod(i)) for  i in range(0,max_id/10000+1)]
    zixun_info=[(i,datetime.datetime.fromtimestamp(j).strftime("%Y-%m-%d %H:%M:%S")) for i,j in zixun_info if j ]


    _=Product.objects.all().order_by("-pid")[0]
    max_id=_.pid
    product_info=[(i,get_product_sitemap_lastmod(i)) for  i in range(0,max_id/10000+1)]
    product_info=[(i,datetime.datetime.fromtimestamp(j).strftime("%Y-%m-%d %H:%M:%S")) for i,j in product_info if j ]

    _=Ask.objects.all().order_by("-askid")[0]
    max_id=_.askid
    ask_info=[(i,get_ask_sitemap_lastmod(i)) for  i in range(0,max_id/10000+1)]
    ask_info=[(i,datetime.datetime.fromtimestamp(j).strftime("%Y-%m-%d %H:%M:%S")) for i,j in ask_info if j ]

    _=News.objects.all().order_by("-nid")[0]
    max_id=_.nid
    news_info=[(i,get_news_sitemap_lastmod(i)) for  i in range(0,max_id/10000+1)]
    news_info=[(i,datetime.datetime.fromtimestamp(j).strftime("%Y-%m-%d %H:%M:%S")) for i,j in news_info if j ]
    return render_to_response("sitemap/sitemap_index.html", locals(),mimetype="text/xml")

def zixun_sitemap_xml(request,id):
    id=int(id)
    info=Consult.objects.filter(zid__gte=id*10000,zid__lt=(id+1)*10000).values("zid","addtime")
    info=[[i["zid"],datetime.datetime.fromtimestamp(i["addtime"]).strftime("%Y-%m-%d")]  for i in info ]
    return  render_to_response("sitemap/zixun_sitemap_xml.html",locals(),mimetype="text/xml")

def product_sitemap_xml(request,id):
    id=int(id)
    info=Product.objects.filter(pid__gte=id*10000,pid__lt=(id+1)*10000).values("pid","addtime")
    info=[[i["pid"],datetime.datetime.fromtimestamp(i["addtime"]).strftime("%Y-%m-%d")]  for i in info ]
    return  render_to_response("sitemap/product_sitemap_xml.html",locals(),mimetype="text/xml")

def ask_sitemap_xml(request,id):
    id=int(id)
    info=Ask.objects.filter(askid__gte=id*10000,askid__lt=(id+1)*10000).values("askid","ask_time")
    info=[[i["askid"],datetime.datetime.fromtimestamp(i["ask_time"]).strftime("%Y-%m-%d")]  for i in info ]
    return  render_to_response("sitemap/ask_sitemap_xml.html",locals(),mimetype="text/xml")

def news_sitemap_xml(request,id):
    id=int(id)
    info=News.objects.filter(nid__gte=id*10000,nid__lt=(id+1)*10000).values("nid","addtime")
    info=[[i["nid"],datetime.datetime.fromtimestamp(i["addtime"]).strftime("%Y-%m-%d")]  for i in info ]
    return  render_to_response("sitemap/news_sitemap_xml.html",locals(),mimetype="text/xml")