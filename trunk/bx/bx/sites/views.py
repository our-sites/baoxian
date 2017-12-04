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
import traceback

def index(request):
    id=request.get_host().split(".")[0]
    user=MyUser.objects.get(uid=int(id))
    assert user.is_proxy==1

    try:
        _=Company.objects.get(cid=user.proxy_cid)
        user.comname=_.comname
        user.comcontent=_.content
        user.video_id=_.get_video_id()
    except:
        traceback.print_exc()
        user.comname=""
        user.comcontent=""
        user.video_id=None

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
    advices=Advice.objects.all().order_by("-iid")
    shares=Share.objects.all().order_by("-sid")
    adds=Add.objects.all().order_by("-aid")
    asks_withans=Ask.objects.filter(ans_num__gt=0).order_by("-ask_time")
    for i in my_shares:
        i.company_info=company_info[i.cid]

    return  render_to_response("sites_index.html",locals(),
                               context_instance=RequestContext(request))

def add_adivce(request):
    get_info=request.GET
    post_info=request.POST
    phone=post_info.get("cellphone")
    text=post_info.get("text")
    name=post_info.get("name","")
    next=post_info.get("next","/")
    uid=post_info.get("uid")
    uid=int(uid)
    print "uid",uid

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
                     city_id=request.city_id,name=name,touid=uid)
            _.save()
            _.send_success_add_sms()
            if request.province or request.city:
                request.send_allsite_msg("来自%s的用户提交了一份一对一咨询"%(request.province+request.city))
            if not request.GET.has_key("site"):
                data={"errorCode":0,"msg":"咨询提交成功！","formSuccess":{"redirect":next ,
                                                                 "duration":1000},"data":{}}
            else:
                data={"status":True,"msg":"咨询提交成功！"}

    return HttpResponse(json.dumps(data),mimetype="application/javascript")
