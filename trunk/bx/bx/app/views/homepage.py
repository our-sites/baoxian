#coding:utf-8
# write  by  zhou
# 个人主页
from bx.utils.aes import *
from bx.decorators import *
from bx.models import Ask,Answer
from bx import  settings
import  datetime
from bx.myauth.models import *

@app_api(login_required=True)
def index(request):
    '''个人主页API
    参数
    uid   int,必传, 用户ID
    返回结果:
    正常情况下:
    根据uid的不同,返回的数据分为两种,代理人 投保人, 二者所拥有的个人信息是不同的,所返回的数据内容也是稍有不同
    a.当该用户是代理人时候
    {
     "errorCode": 0,
     "formError": {},
     "message": "",
     "data": {
      "coin_num": 0,   #积分数目
      "works": [{"comname":"保险代理公司",
                  "position":"经理",
                  "startdate":"2017-01-01",
                  "enddate":"2017-02-01"}],     #工作经历,是一个列表,如果无工作经历,那么就是一个空列表
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
      "recent_ans": #我最近的回答, 是一个列表 ,本接口返回了10个, 展示的时候可以按照自己的需要进行截取.
      [
       {
        "askid": 287,   #回答对应的问题的ID
        "ask_content": "\u6211\u8981\u5916\u51fa\u4e09\u4e2a\u6708\u5de5\u5730\u4e0a\u5de5\u4f5c", #问题的描述
        "ans_content": "\u610f\u5916\u9669\u5fc5\u987b\u8981\u4e70\u7684"    #我的回答
       },
       {
        "askid": 281,
        "ask_content": "\u4e70\u7684\u5e73\u5b89\u4fdd\u9669\uff0c\u670d\u52a1\u7ecf\u7406\u5df2\u79bb\u804c",
        "ans_content": "\u6ca1\u5f71\u54cd"
       },
       {
        "askid": 276,
        "ask_content": "\u5728\u624b\u673a\u4e0a\u5e2e\u6211\u4e70\u4e86\u4fdd\u9669\uff0c\u94f6\u884c",
        "ans_content": "\u5728\u72b9\u8c6b\u671f\u5185\u4fdd\u8d39\u662f\u5168\u90e8\u8fd4\u8fd8\u7684"
       },
       {
        "askid": 291,
        "ask_content": "\u513f\u5b50\u7ed9\u7236\u4eb2\u4e70\u4fdd\u9669\u513f\u5ab3\u5987\u662f\u53d7\u76ca",
        "ans_content": "\u53ef\u4ee5\u6210\u7acb"
       },
       {
        "askid": 509,
        "ask_content": "\u533b\u7597\u4fdd\u9669\u62a5\u9500\u53ea\u80fd\u5f53\u5730\u62a5\u9500\u5417",
        "ans_content": "\u60a8\u597d\u533b\u7597\u4fdd\u9669\u662f\u4e0d\u80fd\u91cd\u590d\u62a5\u9500\u7684\uff0c"
       },
       {
        "askid": 712,
        "ask_content": "23\u5c81\u7537\u5b69\uff0c\u60f3\u4fdd\u4e2a\uff0c\u975e\u5e38\u5168\u9762\uff0c\u8d39\u7528",
        "ans_content": "\u60a8\u597d\uff01\u4e0d\u540c\u516c\u53f8\u4e07\u80fd\u9669\u7684\u56de\u62a5\u7387\u662f"
       },
       {
        "askid": 832,
        "ask_content": "\u5728\u5916\u5730\u4f4f\u9662\uff0c\u5982\u679c\u6211\u53bb\u590d\u5370\u75c5\u5386\uff0c",
        "ans_content": "\u804c\u5de5\u533b\u7597\u62a5\u9500\u6bd4\u4f8b\uff0c\u4f1a\u6bd4\u5c45\u6c11"
       }
      ],
      "imgs": [],      #我的相册, 是一个列表,列表内每个元素是一个url
      "proxy_comname": "\u4fe1\u8bda\u4eba\u5bff\u4fdd\u9669\u6709\u9650\u516c\u53f8",
      "sex": 1,      #性别   1  代表 男   2代表女     0代表未知
      "ans_num": 518   #我的回答数
     }
    }
    b.当用户是投保人时
    {
     "errorCode": 0,
     "formError": {},
     "message": "",
     "data": {
      "coin_num": 0,  #积分数目
      "uid": 1753,   #用户ID
      "recent_ask":  #最近提交的问题   是一个列表 ,本接口返回了10个, 展示的时候可以按照自己的需要进行截取.
      [
       {
        "askid": 7869,   #问题ID
        "ask_content": "\u5bb6\u91cc\u67093\u5c81\u7684\u5b9d\u5b9d\uff0c\u8bf7\u63a8\u8350\u4e00\u4efd\u9002", #问题描述
        "ans_content": null  #问题最近的回答, 如果没有任何回答,这个值为null
       },
       {
        "askid": 7752,
        "ask_content": "\u60f3\u7ed9\u4e00\u5bb6\u4e09\u53e3\u8d2d\u4e70\u4fdd\u9669\uff0c\u7238",
        "ans_content": "\u4f60\u597d\uff0c\u6211\u662f\u592a\u5e73\u6d0b\u9ad8\u7ea7\u987e\u95ee"
       },
       {
        "askid": 7589,
        "ask_content": "\u6211\u4e70\u4e86\u5e73\u5b89\u667a\u80dc\u4eba\u751f\u4e07\u80fd\u578b",
        "ans_content": "\u6ca1\u6709\u6307\u5b9a\u53d7\u76ca\u4eba\uff0c\u53d7\u76ca\u8005\u5c31"
       },
       {
        "askid": 7420,
        "ask_content": "\u53ef\u4ee5\u66f4\u6539\u6295\u4fdd\u4eba\u5417\uff1f\u6bd4\u5982\u5988",
        "ans_content": "\u8981\u770b\u4f60\u7684\u7f34\u8d39\u671f\u9650\u662f\u591a\u957f\u65f6"
       },
       ...
      ],
      "sex": 0, #性别   1  代表 男   2代表女     0代表未知
      "imgs": [], #我的相册, 是一个列表,列表内每个元素是一个url
      "img": "https://www.bao361.cn/media/userimgurl/1.jpg", #头像URL
      "area": "--",    #所在地区
      "coin_rank": 0,  #积分排行
      "age": 35,    #年龄
      "real_name": "\u5468\u65b0\u9e4f", #真实姓名
      "vphone": 1,   #是否通过手机认证
      "vweixin": 1,  #是否通过微信认证
      "myad": "\u6682\u672a\u5b8c\u5584\u8be5\u4fe1\u606f"  #我的个人介绍
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
    if is_proxy:
        _ = user.get_comobj()
        if _:
            proxy_comname = _.comname
            proxy_cid = _.cid
        else:
            proxy_comname = "暂未完善该信息"
            proxy_cid = 0
        works = UserWorkInfo.objects.filter(uid=user.uid,status=1)
        works = [{"comname": i.get_company_object().comname,
                  "position": i.position,
                  "startdate": i.startdate,
                  "enddate": i.enddate}  for i in works]
        if not works:
            works = [{"comname": "保险代理公司",
                     "position": "经理",
                     "startdate": "2017-01-01",
                     "enddate": "2017-02-01"}]
        #answers = MyUser.
        my_ans = Answer.objects.filter(uid=user.uid)[:10]
        my_ans_ask = Ask.objects.filter(askid__in=set([i.askid  for i in my_ans]))
        my_ans_ask_dict = dict([(i.askid,i) for i in my_ans_ask])
        ans_num = user.ans_num
        recent_ans = [{"askid":i.askid,"ask_content":my_ans_ask_dict[i.askid].ask_content,
                       "ans_content":i.ans_content}  for i in my_ans]
        return {"img": img, "real_name": real_name,
                "sex": sex, "imgs": imgs,
                "coin_num": coin_num,
                "coin_rank": coin_rank,
                "age": age,
                "area": area, "myad": myad,
                "proxy_comname": proxy_comname,
                "proxy_cid": proxy_cid,
                "works": works,
                "recent_ans": recent_ans,
                "ans_num": ans_num,
                "vphone": vphone,
                "uid": int(uid),
                "vweixin": vweixin}
    else:
        recent_ask = []
        for i in Ask.objects.filter(uid=user.uid).order_by("-askid")[:10]:
            _ans = i.get_last_ans()
            if _ans:
                _ans_content = _ans.ans_content
            else:
                _ans_content = None
            recent_ask.append({ "askid": i.askid,
                                "ask_content": i.ask_content,
                                "ans_content": _ans_content  })
        return {"img": img,
                "real_name": real_name,
                "sex": sex,
                "imgs": imgs,
                "coin_num": coin_num,
                "coin_rank": coin_rank,
                "age": age,
                "area": area,
                "myad": myad,
                "vphone": vphone,
                "recent_ask": recent_ask,
                "uid": int(uid),
                "vweixin": vweixin}
