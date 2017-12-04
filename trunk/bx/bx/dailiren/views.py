#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/11/15.
# ---------------------------------
from django.shortcuts import  render_to_response
from django.template.context import  RequestContext
from django.http import  HttpResponseRedirect,HttpResponse
from bx.models import *
from django.core.paginator import  Paginator
from  bx.myauth.models import *
from django.conf import  settings
from bx.decorators import mobile_browser_adaptor_by_host

def index(request):
    return HttpResponseRedirect("/dailiren/search/")

@mobile_browser_adaptor_by_host(settings.M_HOST_FUN,{"dailiren_search.html":"m_dailiren_search.html"})
def search(request):
    company_list=Company.objects.all()
    path=request.path
    page=re.search(r"/(\d+)\.html",path)
    if page:
        page=int(page.groups()[0])
    else:
        page=1
    _info=re.search(r"/(\d+)-(\d+)",path)
    if _info:
        city_id,c_id=tuple(_info.groups())
        city_id=int(city_id)
        c_id=int(c_id)
    else:
        city_id=0
        c_id=0
    if request.path=="/dailiren/search" or request.path=="/dailiren/search/" :
        if request.city_id:
            city_id=request.city_id
    if c_id:
        c_obj=Company.objects.get(cid=c_id)
    else:
        c_obj=None
    if city_id:
        city_obj=Area.objects.get(id=city_id)
    company_list=Company.objects.all().order_by("-dailiren_weight")[:25]
    params={}

    if c_id:
        params["proxy_cid"]=c_id

    if city_id:
        params["city_id"]=int(city_id)


    objs=MyUser.objects.filter(is_proxy=1, proxy_cid__gt=0,**params).order_by("-ans_num","uid")
    paginator=Paginator(objs,9)
    info=paginator.page( page)
    allinfo=info
    area_ids=[ i.province_id  for i in allinfo  if i.province_id  ]+[i.city_id for i in allinfo if i.city_id]
    area_info=dict([(i["id"],i["areaname"]) for i in  Area.objects.filter(id__in=area_ids).values("id","areaname")])
    for i in allinfo:
        i.province_city_info=''
        if i.province_id:
            i.province_city_info+=area_info[i.province_id]
        if i.city_id:
            i.province_city_info+=area_info[i.city_id]

    return  render_to_response("dailiren_search.html",locals(),
                               context_instance=RequestContext(request))


@mobile_browser_adaptor_by_host(settings.M_HOST_FUN,{"dailiren_detail.html":"m_dailiren_detail.html"})
def detail(request,id):
    #id=request.get_host().split(".")[0]
    user=MyUser.objects.get(uid=int(id))
    assert user.is_proxy==1

    try:
        _=Company.objects.get(cid=user.proxy_cid)
        user.comname=_.comname
        user.comcontent=_.content
    except:
        user.comname=""
        user.comcontent=""

    products=Product.objects.filter(cid=user.proxy_cid)[:10]

    my_ans=Answer.objects.filter(uid=user.uid)
    _dict = dict([(_.askid,_.ans_content) for _ in my_ans])
    my_ans_ask=Ask.objects.filter(askid__in=[ i.askid for i in my_ans]).order_by("-ask_time")[:10]
    for _ in my_ans_ask:
        _.self_content=_dict[_.askid]

    degree_info=dict(AddDegree.objects.all().values_list("adid","info"))
    money_info=dict(AddMoney.objects.all().values_list("amid","info"))
    position_info=dict(AddPosition.objects.all().values_list("apid","info"))
    company_info=dict(Company.objects.all().values_list("cid","comname"))
    xinwen_info = Consult.objects.filter(type=4, status=1).order_by("-addtime")[:7]
    anli_info = Consult.objects.filter(type=2, status=1).order_by("-addtime")[:7]
    my_adds=Add.objects.filter(uid=user.uid).order_by("-uptime")
    for i in my_adds:
        i.degree_info=degree_info[i.adid]
        i.money_info=money_info[i.amid]
        i.position_info=position_info[i.apid]
        i.company_info=company_info[i.cid]

    my_shares=Share.objects.filter(uid=user.uid).order_by("-uptime")
    dingzhis=DingZhi.objects.all().order_by("-did")
    for i in my_shares:
        i.company_info=company_info[i.cid]

    return  render_to_response("dailiren_detail.html",locals(),
                               context_instance=RequestContext(request))

def add_adivce(request):
    get_info=request.GET
    post_info=request.POST
    phone=post_info.get("cellphone")
    text=post_info.get("text")
    name=post_info.get("name","")
    next=post_info.get("next","/")
    phone=phone.strip()
    try:
        assert len(phone)==11
        phone=int(phone)
    except:
        if not  request.GET.has_key("site"):
            data={"errorCode":500,"formError":{"fields":[{"name":"cellphone","msg":"手机号格式不正确！"}]}}
        else:
            data={"status":False,"msg":"手机号格式不正确"}
    else:
        if not text:
            if not request.GET.has_key("site"):
                data={"errorCode":500,"formError":{"fields":[{"name":"text","msg":"内容必须填写！"}]}}
            else:
                data={"status":False,"msg":"内容必须填写"}
        else:
            _=Advice(phone=phone,content=text,ip=request.ip,province_id=request.province_id,
                     city_id=request.city_id,name=name)
            _.save()
            _.send_success_add_sms()
            if request.province or request.city:
                request.send_allsite_msg("来自%s的用户提交了一份保险咨询"%(request.province+request.city))
            if not request.GET.has_key("site"):
                data={"errorCode":0,"msg":"咨询提交成功！","formSuccess":{"redirect":next ,
                                                                 "duration":1000},"data":{}}
            else:
                data={"status":True,"msg":"咨询提交成功！"}

    return HttpResponse(json.dumps(data),mimetype="application/javascript")
