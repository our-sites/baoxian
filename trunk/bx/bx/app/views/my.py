#coding:utf-8
# write  by  zhou
from bx.utils.aes import *
from bx.decorators import *
from bx.models import Ask,Answer,Advice,Add,Share,AdviceReply
from bx import  settings
import  datetime
import base64
from bx.myauth.models import *
from bx.utils.sms import send_dayysms_validnumber
from django.core.files.uploadedfile import InMemoryUploadedFile,File,SimpleUploadedFile

@app_api(login_required = True)
def change_password_get_validated_phone(request):
    '''
    修改密码--获取用户已认证的手机号
    参数:
    无
    返回数据:
    两种类型:
    a.用户已经通过了手机号认证
    {"errorCode":0,"formError":{},"data":18749679769,"message":""}
    b.用户未通过手机号认证
    {"errorCode":0,"formError":{},"data":null,"message":""}
    '''
    if request.myuser.phone :
        return request.myuser.phone
    else:
        return None


@app_api(login_required=True)
def change_password_phone_valid(request):
    '''
    修改密码-- 如果用户无已认证手机号,验证用户填入的手机号是否可用
    参数:
    phone  手机号
    返回类型:
    a.手机号不合法
    {"errorCode":0,"formError":{"phone":"手机号不合法"},"data":null,"message":"手机号不合法"}
    b.手机号被占用
    {"errorCode":0,"formError":{},"data":false,"message":""}
    c.手机号可用
    {"errorCode":0,"formError":{},"data":true,"message":""}
    '''
    phone = request.POST.get("phone","")
    if not phone:
        raise FieldError("phone","手机号不能为空!")
    try:
        phone = int(phone.strip())
        assert len((str(phone))) == 11
    except:
        raise FieldError("phone","手机号不合法!")
    _ = MyUser.objects.filter(phone=int(phone)).count()
    if _:
        return False
    else:
        return True


@app_api(login_required=True)
def change_password_send_sms_number(request):
    '''修改密码--发送验证码
    参数:
    phone   手机号
    返回类型:
    a.手机号不合法
    {"errorCode":0,"formError":{"phone":"手机号不合法"},"data":null,"message":"手机号不合法"}
    b.发送成功
    {"errorCode":0,"formError":{},"data":true,"message":""}
    '''
    phone = request.POST.get("phone","")
    if not phone:
        raise FieldError("phone","手机号不能为空!")
    try:
        phone = int(phone.strip())
        assert len((str(phone))) == 11
    except:
        raise FieldError("phone","手机号不合法!")
    valid_number = "".join(random.sample([str(i) for i in range(1,10)],6))
    send_dayysms_validnumber(phone,valid_number)
    request.appsession["my_resetpwd_validnumber"] = valid_number
    return True


@app_api(login_required=True)
def change_password_sms_number_valid(request):
    '''修改密码--验证验证码是否正确
    参数:
    number   验证码 ,必填
    返回类型:
    a.验证码正确
    {"errorCode":0,"formError":{},"data":true,"message":""}
    b.验证码不正确
    {"errorCode":0,"formError":{},"data":false,"message":""}
    '''
    number = request.POST.get("number","").strip()
    if request.appsession.get("my_resetpwd_validnumber") == number :
        return True
    else:
        return False


@app_api(login_required=True)
def change_password_confirm(request):
    '''修改密码 -- 提交
    参数:
    phone      手机号
    number     验证码
    password   新密码(必须不小于6位)
    返回类型:
    a.验证码不正确
    {"errorCode":0,"formError":{"number":"验证码不正确"},"data":null,"message":"验证码不正确"}
    b.密码不合法
    {"errorCode":0,"formError":{"password":"密码不合法"},"data":null,"message":"密码不合法"}
    c.手机号不合法(原因可能是手机号格式不正确 或者 手机号已被占用)
    {"errorCode":0,"formError":{"phone":"手机号已被占用"},"data":null,"message":"手机号已被占用"}
    d.密码重置成功
    {"errorCode":0,"formError":{},"data":true,"message":""}
    '''
    post_info = request.POST
    phone = post_info.get("phone","").strip()
    numer = post_info.get("number","").strip()
    password = post_info.get("password","").strip()
    if numer != request.appsession.get("my_resetpwd_validnumber"):
        raise FieldError("number","验证码不正确")
    if len(password)<6:
        raise FieldError("password","密码长度不能小于6位!")
    if request.myuser.phone :
        request.myuser.reset_password(password)
        return  True
    else:
        try:
            _phone = int(phone)
            len(str(_phone)) == 11
        except:
            raise FieldError('phone', "手机号格式不正确")
        try:
            MyUser.objects.get(phone=int(phone))
            raise FieldError("phone", "该手机号已被占用")
        except MyUser.DoesNotExist:
            request.myuser.phone = _phone
            request.myuser.save()
            request.myuser.reset_password(password)
            return True


@app_api(login_required=True)
def my_uid(request):
    '''获取当前登录用户的uid
    参数:
    无
    返回值:
    {"errorCode":0,"formError":{},"data":123,"message":""}
    '''
    return request.myuser.uid


@app_api(login_required=True)
def my_info(request):
    '''我的个人信息 API
    参数:
    无
    返回结果:
    {
     "errorCode": 0,
     "formError": {},
     "message": "",
     "data": {
      "coin_num": 0,   #积分数目
      "proxy_cid": 70, #所在保险公司的ID
      "uid": 2160,     #用户的uid
      "img": "https://www.bao361.cn/media/userimgurl/%E6%9D%8E%E5%BC%BA0.jpg", #头像URL
      "area": "\u5317\u4eac\u5317\u4eac\u5e02",   #所在地区
      "coin_rank": 0,   #积分排行
      "age": 33,   #年龄
      "real_name": "\u674e\u5f3a", #真实姓名
      "vphone": 1,  #是否通过手机认证
      "vweixin": 1, #是否通过微信认证
      "myad": "\u6682\u672a\u5b8c\u5584\u8be5\u4fe1\u606f", #我的个人简介
      "imgs": [],      #我的相册, 是一个列表,列表内每个元素是一个url
      "proxy_comname": "\u4fe1\u8bda\u4eba\u5bff\u4fdd\u9669\u6709\u9650\u516c\u53f8",
      "sex": 1,      #性别   1  代表 男   2代表女     0代表未知
      "ans_num": 518   #我的回答数
     }

    }


    '''
    uid = request.POST.get('uid',"")
    if not uid:
        raise FieldError("uid","uid不能为空")
    user = MyUser.objects.get(uid=int(uid))
    now = datetime.datetime.now()
    img = user.get_img_url()
    if not  img.startswith("http"):
        img = img
    real_name = user.real_name or "匿名用户"
    sex = user.sex
    imgs =[ i.photo.url for i in  UserPhoto.objects.filter(uid=user.uid,status=1)\
                                      .order_by("-uptime")[:10] ]
    coin_num = user.get_coin_num()
    coin_rank = user.get_coin_rank()
    is_proxy = user.is_proxy
    if user.birthday:
        age = (now.year - datetime.datetime.strptime(user.birthday,"%Y-%m-%d").year)
    else:
        age = "保密"
    area = user.get_province_city_info() or "--"
    myad = user.proxy_myad or "暂未完善该信息"
    vphone = user.vphone
    vweixin = user.vweixin
    _ = user.get_comobj()
    if _:
        proxy_comname = _.comname
        proxy_cid = _.cid
    else:
        proxy_comname = "暂未完善该信息"
        proxy_cid = 0
    ans_num = user.ans_num
    return {"img": img, "real_name": real_name,
            "sex": sex, "imgs": imgs,
            "coin_num": coin_num,
            "coin_rank": coin_rank,
            "age": age,
            "area": area, "myad": myad,
            "proxy_comname": proxy_comname,
            "proxy_cid": proxy_cid,
            "ans_num": ans_num,
            "vphone": vphone,
            "uid": int(uid),
            "vweixin": vweixin}


@app_api(login_required=True)
def my_validate(request):
    '''我已完成的认证
    参数:
    无
    返回值:
    a.未完成任何认证
    {"errorCode":0,"formError":{},"data":[],"message":""}
    a.完成了部分认证(vphone代表手机号认证 vweixin代表微信认证)
    {"errorCode":0,"formError":{},"data":["vphone","vweixin"],"message":""}
    '''
    result = []
    if request.myuser.vphone:
        result.append("vphone")
    if request.myuser.vweixin:
        result.append("vweixin")
    return result


@app_api(login_required=True)
def my_validate_phone_valid(request):
    '''手机认证 --验证手机号是否可用
    参数:
    phone  手机号
    返回类型:
    a.手机号不合法
    {"errorCode":0,"formError":{"phone":"手机号不合法"},"data":null,"message":"手机号不合法"}
    b.手机号被占用
    {"errorCode":0,"formError":{},"data":false,"message":""}
    c.手机号可用
    {"errorCode":0,"formError":{},"data":true,"message":""}
    '''
    phone = request.POST.get("phone","")
    if not phone:
        raise FieldError("phone","手机号不能为空!")
    try:
        phone = int(phone.strip())
        assert len((str(phone))) == 11
    except:
        raise FieldError("phone","手机号不合法!")
    _ = MyUser.objects.filter(phone=int(phone)).count()
    if _:
        return False
    else:
        return True


@app_api(login_required=True)
def my_validate_phone_send_sms_number(request):
    '''手机认证 --获取验证码
    参数:
    phone   手机号
    返回类型:
    a.手机号不合法
    {"errorCode":0,"formError":{"phone":"手机号不合法"},"data":null,"message":"手机号不合法"}
    b.发送成功
    {"errorCode":0,"formError":{},"data":true,"message":""}
    '''
    phone = request.POST.get("phone","")
    if not phone:
        raise FieldError("phone","手机号不能为空!")
    try:
        phone = int(phone.strip())
        assert len((str(phone))) == 11
    except:
        raise FieldError("phone","手机号不合法!")
    valid_number = "".join(random.sample([str(i) for i in range(1,10)],6))
    send_dayysms_validnumber(phone,valid_number)
    request.appsession["my_validate_phone_validnumber"] = valid_number
    return True


@app_api(login_required=True)
def my_validate_phone_sms_number_valid(request):
    '''手机认证 -- 验证验证码是否正确
    参数:
    number   验证码
    返回类型:
    a.验证码正确
    {"errorCode":0,"formError":{},"data":true,"message":""}
    b.验证码不正确
    {"errorCode":0,"formError":{},"data":false,"message":""}
    '''
    number = request.POST.get("number","").strip()
    if request.appsession.get("my_validate_phone_validnumber") == number :
        return True
    else:
        return False


@app_api(login_required=True)
def my_validate_phone_confirm(request):
    '''手机认证 -- 提交
    参数:
    phone  手机号
    number 验证码
    '''
    post_info = request.POST
    phone = post_info.get("phone","")
    number = post_info.get('number',"")
    try:
        phone = int(phone)
        len(str(phone)) == 11
    except:
        raise FieldError("phone","手机号格式不正确")
    if not   request.appsession.get("my_validate_phone_validnumber") == number :
        raise FieldError("number","验证码不正确")
    try:
        MyUser.objects.get(phone=phone)
    except MyUser.DoesNotExist:
        request.myuser.phone = phone
        request.myuser.vphone = 1
        request.myuser.save()
        return True
    else:
        raise FieldError("phone","该手机号已被占用")


@app_api(login_required=True)
def my_validate_weixin_confirm(request):
    '''微信认证 -- 提交'''
    post_info = request.POST


@app_api(login_required=True)
def my_messages_unread_num(request):
    '''我的消息--获取未读消息数目
    参数:
    无
    返回值:
    {"errorCode":0,"formError":{},"data":123,"message":""}
    '''
    return request.myuser.get_unread_messages().count()


@app_api(login_required=True)
def my_messages_all_message(request):
    '''我的消息---获取所有消息
    参数:
    max_msgid 最大消息id, 非必填
    num       获取的个数,必填
    返回值:
    {
     "errorCode": 0,
     "formError": {},
     "message": "",
     "data": [
      {
       "content": "fsdafdsafdsafdsafdsfddsf",  #消息内容
       "msgid": 109,    #消息ID
       "is_read": 1,    #是否已读, 1代表已读 0代表未读
       "addtime": 1486378632,    #创建时间戳
       "subject": "test"   #消息标题
      },
      {
       "content": "testtesttest",
       "msgid": 108,
       "is_read": 1,
       "addtime": 1486378092,
       "subject": "test"
      },
      {
       "content": "fsdafdsafdsafdsafdsfddsf",
       "msgid": 86,
       "is_read": 1,
       "addtime": 1486285681,
       "subject": "test"
      }
     ]
    }
    '''
    uid = request.myuser.uid
    max_msgid = request.POST.get("max_msgid","")
    num = request.POST.get("num",'')
    try:
        num = int(num)
    except:
        raise FieldError("num","num必须为整数")
    if not max_msgid:
        msgs = Msg.objects.filter(uid = uid).order_by("-msgid")[:num]
    else:
        try:
            max_msgid = int(max_msgid)
        except:
            raise  FieldError("max_msgid","max_msgid必须为整数")
        msgs = Msg.objects.filter(uid = uid,msgid__lt = max_msgid).order_by("-msgid")[:num]
    return [{"msgid": i.msgid,
             "content": i.message,
             "subject": i.subject,
             "addtime": i.addtime,
             "is_read": i.is_read} for i in msgs]


@app_api(login_required=True)
def my_messages_set_all_read(request):
    '''我的消息 -- 设置所有消息已读
    参数:
    无
    返回值:
    {"errorCode":0,"formError":{},"data":true,"message":""}
    '''
    request.myuser.get_unread_messages().update(is_read = 1)
    return True


@app_api(login_required=True)
def my_photo_all_phono(request):
    '''我的相册 -- 我的所有图片
    参数:
    无
    返回值:
    {"errorCode":0,
    "formError":{},
    "data":[
            {
            "id":1,    #图片id
            "photo_url": "https://upyun.bao361.cn/xx", #图片的url
            "addtime": 1486285681   #图片创建时候的时间戳
            }
            ],
    "message":""}
    '''
    _ =UserPhoto.objects.filter(uid=request.myuser.uid,status=1).order_by("-pid")[:50]
    return [{"id": i.id,
             "photo_url": i.photo.url,
             "addtime": i.addtime} for i in _]


@app_api(login_required=True)
def my_photo_add(request):
    '''我的相册 - 添加图片
    img_name   图片名 ,必传 ,如 a.png
    img_b64_data 图片的base64数据,必传
    返回值:
    {"errorCode":0,"formError":{},"data":{"pid":11,"url":"https://upyun.bao361.cn/xxx.png"},"message":""}
    '''
    post_info = request.POST
    img_name = post_info.get("img_name","")
    assert  "." in img_name
    img_name = str(int(time.time())) + "." + img_name.split(".")[-1]
    img_b64_data = post_info.get("img_b64_data","")
    img_data = base64.b64decode(img_b64_data)
    img_file = SimpleUploadedFile(img_name,img_data)
    _ = UserPhoto(uid=request.myuser.uid, photo=img_file)
    _.save()
    return {"pid": _.pid, "url": _.photo.url}


@app_api(login_required=True)
def my_photo_del(request):
    '''我的相册 - 删除单个图片
    参数:
    pid   图片的pid
    返回值:
    {"errorCode":0,"formError":{},"data":true,"message":""}
    '''
    post_info = request.POST
    pid = post_info.get("pid","")
    try:
        pid = int(pid)
    except:
        raise FieldError("id","id必须为整数")
    photo = UserPhoto.objects.get(pid=pid)
    photo.status = 4
    photo.save()
    return True


@app_api(login_required=True)
def my_photo_multi_del(request):
    '''我的相册 - 删除多个图片
    参数:
    pids   图片的pid,逗号分割. 比如:    1,2,3
    返回值:
    {"errorCode":0,"formError":{},"data":true,"message":""}
    '''
    post_info = request.POST
    pid = post_info.get("pids","")
    pids = pid.split(",")
    _ = []
    for i in pids:
        try:
            _.append(int(i))
        except:
            pass
    photo_queryset = UserPhoto.objects.filter(pid__in=_)
    photo_queryset.update(status=4)
    return True


@app_api(login_required=True)
def my_ans_all(request):
    '''我的回答
    参数:
    max_ansid 回答的最大id,非必填,int
    num       获取的数目,必填,int
    返回数据说明:

    '''
    user = request.myuser
    max_ansid = request.POST.get("max_ansid","")
    max_ansid = int(max_ansid)
    num = request.POST.get("num",'')
    num = int(num)
    my_ans = Answer.objects.filter(uid=user.uid,ansid__lt=max_ansid)[:num]
    my_ans_ask = Ask.objects.filter(askid__in=set([i.askid  for i in my_ans]))
    my_ans_ask_dict = dict([(i.askid,i) for i in my_ans_ask])
    ans_num = user.ans_num
    ans = []
    for i in my_ans:
        _user = i.get_user()
        ans.append({"askid": i.askid,
                    "ask_content": my_ans_ask_dict[i.askid].ask_content,
                    "ans_content": i.ans_content,
                    "ansid": i.ansid,
                    "ans_time": i.ans_time,
                    "ask_user_uid": _user.uid,
                    "ask_user_name": _user.get_hide_namecontent(),
                    "ask_user_img_url": _user.get_img_url(),
                    "ans_user_uid": user.uid,
                    "ans_user_name": user.get_hide_namecontent(),
                    "ans_user_img_url": user.get_img_url()})
    return {"ans_num": ans_num,
             "ans_list": ans}


@app_api(login_required=True)
def  my_advice_all(request):
    '''我的客户咨询 --获取所有
    参数:
    无
    返回数据说明:

    '''
    user = request.myuser
    _ = Advice.objects.filter(touid=user.uid).order_by("-iid")
    return [{"id": i.iid,
             "content": i.content,
             "phone": i.phone,
             "is_replyed": i.is_replyed,
             "addtime": i.addtime} for i in _]


@app_api(login_required=True)
def my_advice_detail(request):
    '''
    我的客户咨询 -- 获取单个咨询的详情
    参数:
    id  必选,int
    返回数据说明:

    '''
    user = request.myuser
    post_info = request.POST
    id = post_info.get("id,","")
    id = int(id)
    _ = Advice.objects.get(iid=id)
    _replys = AdviceReply.objects.filter(iid=_.iid).order_by("-id")
    _by_user = _.get_by_user()
    data = {"id": _.iid,
            "phone": _.phone,
            "content": _.content,
            "addtime": _.addtime,
            "name": _.name or "匿名",
            "img_url": _by_user.get_img_url() if _by_user else "https://upyun.bao361.cn/static/imgs/default-user.png",
            "replys": []
            }
    for i in _replys:
        data["replys"].append({"id":i.id,"content":i.content,"addtime":i.addtime,
                               "img_url":request.myuser.get_img_url()})
    return data


@app_api(login_required=True)
def my_advice_add_reply(request):
    '''我的客户咨询  -- 针对单个咨询进行回复
    参数:
    id 必选,int
    content 必选,char
    返回数据说明:
    {"errorCode":0,"formError":{},"data":true,"message":""}
    '''
    post_info = request.POST
    id = post_info.get("id","")
    content = post_info.get("content","")
    assert id
    assert content
    _ = Advice.objects.get(iid=int(id))
    _.add_reply(content)
    return True


@app_api(login_required=True)
def my_add_all(request):
    "我的增员 -- 获取所有增员"
    post_info = request.POST
    _ = Add.objects.filter(uid=request.myuser.uid)
    result = []
    for i in _:
        request.append({"id": i.id,
                        "title": i.title,
                        "content": i.work_content,
                        "addtime": i.addtime})
    return result

@app_api(login_required=True)
def my_add_add(request):
    "我的增员 --添加"
    post_info = request.POST



@app_api(login_required=True)
def my_add_update(request):
    "我的增员 -- 更新/修改"
    pass

@app_api(login_required=True)
def my_share_all(request):
    "我的签单分享"
    pass

@app_api(login_required=True)
def my_share_add(request):
    "我的签单分享"
    pass

