#coding:utf-8
# write  by  zhou

JsonResponse=lambda x:HttpResponse(json.dumps(x),mimetype="application/javascript")
from bx.decorators import *


#登录
@app_api()
def login(request):
    '''
    功能说明:
    用户登录接口
    参数说明:
    phone
    password
    返回数据说明:
    登录失败:
    {"errorCode":0,"formError":{"phone":"手机号不合法!"},"data":null,"message":"手机号不合法!"}
    登录成功:
    {"errorCode":0,"formError":{},"data":true,"message":""}
    '''
    post_info=request.POST
    print request.body
    phone=post_info.get("phone","")
    password=post_info.get("password","")
    assert phone,FieldError("phone","请输入手机号！")
    assert password,FieldError("password","请输入密码！")
    try:
        phone=int(phone)
    except:
        raise FieldError("phone","手机号不合法!")
    try:
        user=MyUser.objects.get(phone=phone)
    except:
        raise  FieldError("phone","该用户不存在！")
    assert user.is_proxy==1,FieldError("phone",u"账户类型不是保险代理人!")
    if not user.check_password(password):
        raise FieldError("password","密码不正确！")
    user.app_login(request)
    return True

# 三方登录
@app_api()
def login_3(request):
    '''
    功能说明:
    用户三方登录接口(该接口返回结果后,服务端已自动把该用户置为了已登录状态)
    id       三方登录返回的用户ID,通常为一个字符串.(微博的好像是int,qq  weixin的是字符串), 必传,且不能为空字符串!
    type     三方登录类型, 可选值 qq  weixin weibo   ,必传!
    jsoninfo 获取到的用户的所有信息,  字符串 , 必传! 且不能为空字符串!
    注意:
    关于jsoninfo,如果获取到的用户信息是这样的{"unionid":"xx","img_url":"http://xxx"},
    应首先用JSON把这个对象转化为一个字符串 传递到参数中.切记 ,不可直接把这个对象传递过来!!
    返回数据说明:
    成功:
    {"errorCode":0,"formError":{},"data":true,"message":""}
    失败:
    {"errorCode":0,"formError":{"id":"id不能为空"},"data":null,"message":"id不能为空"}
    '''
    post_info=request.POST
    id=post_info.get("id","")
    type=post_info.get("type","")
    jsoninfo=post_info.get("jsoninfo","")
    if not id:
        raise FieldError("id","id不能为空")
    if not type  or  type not in ("qq","weibo","weixin"):
        raise FieldError("type","类型必须是qq weibo  weixin 之一")
    if not jsoninfo:
        raise FieldError('jsoninfo',"jsoninfo必须不为空!")
    user=MyUser.app_oauth(request,type,id,jsoninfo,True)
    user.app_login(request)
    return  True

@app_api()
def is_logined(request):
    '''
    功能说明:
    判断一个用户是否已经登录
    参数说明:
    无参数
    返回数据说明:
    已登录:
    {"errorCode":0,"formError":{},"data":true,"message":""}
    未登录:
    {"errorCode":0,"formError":{},"data":false,"message":""}
    '''
    post_info=request.POST
    if request.myuser:
        return  True
    else:
        return False


#退出登录
@app_api()
def logout(request):
    '''
    功能说明:
    用户退出登录接口
    参数说明:
    无参数
    返回数据说明:
    退出成功:
    {"errorCode":0,"formError":{},"data":true,"message":""}
    '''
    if request.myuser:
        request.myuser.app_logout(request)
    return True
