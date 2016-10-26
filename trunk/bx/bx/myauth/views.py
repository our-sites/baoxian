#coding:utf-8
__author__ = 'zhoukunpeng'
# --------------------------------
# Created by zhoukunpeng  on 2016/7/13.
# ---------------------------------
from decorators import  login_required
from django.conf import  settings
from gcutils.encrypt import  md5
from django.http import  HttpResponseRedirect
from cookie_encrypt import  phpcookie_encode
import  urllib
import time
import  datetime
from django.shortcuts import  render_to_response
from models import  MyUser
from django.template.context import  RequestContext
from django.db.models import  Q
def login(request):
    post_data=request.POST
    next=request.GET.get("next","")
    next=next or  settings.LOGIN_REDIRECT_URL
    if request.method=="POST":
        username=post_data["username"]
        password=post_data["password"]
        timestamp=int(time.time())
        try:
            _tel=int(username)
        except:
            _tel=None
        try:
            if _tel:
                if "@" in username:
                    user=MyUser.objects.get(Q(username=username)|Q(verifymobile=_tel)|Q(email=username))
                else:
                    user=MyUser.objects.get(Q(username=username)|Q(verifymobile=_tel))
            else:
                if "@" in username:
                    user=MyUser.objects.get(username=username|Q(email=username))
                else:
                    user=MyUser.objects.get(username=username)
        except Exception as e :
            print username
            print "Exception",e
            message="该用户不存在！"
        else:
            if user.state!=1:
                message="该用户状态不正常！"
            else:
                if md5(md5(password)+user.salt)==user.password:
                    result=HttpResponseRedirect(next)
                    if isinstance(username,unicode):
                        username=username.encode("utf-8")
                    result.set_cookie("user_info",urllib.quote(
                            phpcookie_encode("\t".join([str(user.supid), username,request.ip,str(timestamp)]),'gc895316')),
                                      domain=".baoxiangj.com")
                    return  result
    return render_to_response(settings.LOGIN_TEMPLATE_NAME,locals(),context_instance=RequestContext(request))


def logout(request):
    result=  HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)
    if request.myuser==None:
        pass
    else:
        result.delete_cookie("user_info",domain=".baoxiangj.com")
    return  result