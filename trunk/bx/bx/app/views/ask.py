#coding:utf-8
# write  by  zhou
JsonResponse=lambda x:HttpResponse(json.dumps(x),mimetype="application/javascript")
from bx.utils.aes import *
from bx.decorators import *
from bx.models import Ask,Answer
from bx import  settings


@app_api(login_required=True)
def ask_list(request):
    '''
    功能说明:
    问吧--获取问吧列表,排序方式askid从大到小, askid越大表明该问题的距离当前时间越短,该问题越新.
    参数说明:
    max_askid  askid的最大值,int,    通过控制此项可以实现加载更多的效果.    非必填项
    type       类型, 取值 0  或 1  2,  0代表全部   1代表已经被回答   2代表尚未被回答,必填项
    num    数量 ,范围0-15,必填项
    返回数据说明:

    比如当传递的参数为:
      num:2   时:
    返回的结果如下:
    {
     "errorCode": 0,
     "formError": {},
     "message": "",
     "data":
    [
      {
       "recent_ans_users":    #最近回答该问题的用户列表
       [
        {
         "province": "\u6d77\u5357",  #省份信息
         "city": "\u6d77\u53e3", #市信息
         "img_url": "https://www.bao361.cn/media/userimgurl/%E5%90%B4%E8%8B%B1%E5%8F%AF.jpg", #头像url
         "name": "\u5434\u82f1\u53ef", #用户名
         "uid": 2012   #用户ID
        },
        {
         "province": "\u91cd\u5e86",
         "city": "\u91cd\u5e86",
         "img_url": "https://www.bao361.cn/media/userimgurl/%E5%8D%A2%E7%99%BB%E7%A2%A7.jpg",
         "name": "\u5362\u767b\u78a7",
         "uid": 2076
        },
        {
         "province": "\u6e56\u5357",
         "city": "\u682a\u6d32",
         "img_url": "https://www.bao361.cn/media/userimgurl/%E8%B0%A2%E7%BE%8E%E4%B8%BD.jpg",
         "name": "\u8c22\u7f8e\u4e3d",
         "uid": 2000
        }
       ],
       "askid": 5413, #问题的ID
       "ask_content": "\u6211\u60f3\u4e70\u610f\u5916\u4fdd\u9669\uff0c\u4eca\u5e74\u4e09\u5341\u516b\uff0c\u4e70\u90a3\u4e00\u79cd\u597d", #问题的详细描述
       "ask_user_info": #提交此问题的用户信息
       {
        "province": "\u798f\u5efa",
        "city": "\u53a6\u95e8",
        "img_url": "https://www.bao361.cn/static/imgs/default-user.png",
        "name": "\u5468\u4ea6\u53ef",
        "uid": 1906
       },
       "ask_time": 1506669284, #问题提交时的时间戳
       "ans_num": 3        #该问题的回答数
      },
      ...
      ...
     ]
    }


    '''
    params={}
    post_info=request.POST
    max_askid=post_info.get("max_askid")
    _type=post_info.get("type")
    num=post_info.get("num")
    try:
        assert num
        num=int(num)
        assert num<=15 and num>0
    except:
        raise FieldError("num","num不合法!num应该0-15范围内")
    if max_askid:
        try:
            max_askid=int(max_askid)
        except:
            raise FieldError("max_askid","max_askid 必须是一个整数")
        params["askid__lt"]=int(max_askid)
    if _type:
        assert _type in ("0","1","2"),FieldError("type","type取值为 0 或 1  或 2")
        if _type == "0":
            pass
        elif _type == "1":
            params["ans_num__gte"] = 1
        else:
            params["ans_num"] = 0
    askobj=Ask.objects.filter(**params).order_by("-askid")[:num]
    askids=[i.askid for i in askobj]
    ansobjs=Answer.objects.filter(askid__in=askids).values("uid","askid","ans_time").order_by("-ans_time")
    ask_uids=[i.uid for i in askobj]
    ans_uids=[i["uid"] for i in ansobjs]
    uids=list(set(ask_uids+ans_uids))
    uid_objs=MyUser.objects.filter(uid__in=uids)
    uid_dict=dict([(int(i.uid),i) for i in uid_objs])
    result=[]
    for i in askobj:
        uid=i.uid
        _={}
        _["ask_user_info"]={"name":uid_dict[int(uid)].get_hide_namecontent(),
                            "province":(settings.AREA_BUFF[int(uid_dict[int(uid)].province_id)]["shortname"]) if uid_dict[int(uid)].province_id else "",
                            "city":(settings.AREA_BUFF[int(uid_dict[int(uid)].city_id)]["shortname"]) if uid_dict[int(uid)].city_id else "",
                            "img_url":uid_dict[int(uid)].get_img_url(),
                            "uid":int(uid)}

        _["ask_content"] = i.ask_content
        _["ans_num"] = i.ans_num
        _["ask_time"]=i.ask_time
        _["recent_ans_users"] = []
        _["askid"]=i.askid
        for j in ansobjs:
            if j["askid"] == i.askid:
                _ans_uid = int(j["uid"])
                _["recent_ans_users"].append({"name":uid_dict[_ans_uid].get_hide_namecontent(),
                            "province":(settings.AREA_BUFF[int(uid_dict[_ans_uid].province_id)]["shortname"]) if uid_dict[_ans_uid].province_id else "",
                            "city":(settings.AREA_BUFF[int(uid_dict[_ans_uid].city_id)]["shortname"]) if uid_dict[_ans_uid].city_id else "",
                            "img_url":uid_dict[_ans_uid].get_img_url(),
                            "uid":_ans_uid})
        result.append(_)
    return  result


@app_api(login_required=True)
def ask_detail(request):
    '''
    功能说明:
    问吧--获取某个问题的详情
    参数说明:
    askid 问题ID,int,必传

    返回数据说明:
    比如当传递的参数为:
    askid:5413 时,
        {
     "errorCode": 0,
     "formError": {},
     "message": "",
     "data": {
      "province": "\u798f\u5efa", #该问题的提问者的省信息
      "city": "\u53a6\u95e8",     #市信息
      "uid": 1906,     #提问者用户ID信息
      "askid": 5413,    #问题的ID
      "ask_content": "\u6211\u60f3\u4e70\u610f\u5916\u4fdd\u9669\uff0c\u4eca\u5e74\u4e09\u5341\u516b\uff0c\u4e70\u90a3\u4e00\u79cd\u597d", #问题详细描述
      "ask_time": 1506669284, #问题提交时间,
      "img_url": "https://www.bao361.cn//static/imgs/default-user.png" #提交此问题的用户的头像
      "ans":    #所有答案的一个列表
      [
       {
        "province": "\u8d35\u5dde", #提交此答案的用户的省信息,
        "ans_content": "\u4f60\u597d\uff01\u610f\u5916\u9669\u5206\u5b58\u94b1\u578b", #答案详情
        "uid": 2022,    #提交此答案的用户ID
        "city": "\u8d35\u9633",  #市信息
        "ans_time": 1506670922, #答案提交时间
        "img_url": "https://www.bao361.cn/media/userimgurl/%E5%AD%99%E6%B5%B7%E9%BA%9F_jxYETU9.jpg", #提交此答案的用户的头像URL
        "ansid": 29769,    #答案ID
        "name": "\u5b59\u6d77\u9e9f",   #提交此答案的用户的用户名
        "good_num":3      #此回答被点赞的次数
       },
        ...
      ]

     }
    }
    '''
    post_info=request.POST
    askid=post_info.get("askid","")
    try:
        askid=int(askid)
    except:
        raise FieldError("askid","askid是必传参数,且为int!")
    ask_obj = Ask.objects.get(askid=askid)
    all_ans=Answer.objects.filter(askid=askid).order_by("-ans_time")
    uids=list(set([ask_obj.uid]+[i.uid for i in all_ans]))
    uid_objs=MyUser.objects.filter(uid__in=uids)
    uid_dict=dict([(i.uid,i) for i in uid_objs])
    result={}
    result["ask_content"]=ask_obj.ask_content
    result["askid"]=ask_obj.askid
    result["uid"]=ask_obj.uid
    result["img_url"]=uid_dict[ask_obj.uid].get_img_url()
    result["ask_time"]=ask_obj.ask_time
    result["province"]=(settings.AREA_BUFF[uid_dict[ask_obj.uid].province_id]["shortname"]) if uid_dict[ask_obj.uid].province_id else ""
    result["city"]=(settings.AREA_BUFF[uid_dict[ask_obj.uid].city_id]["shortname"]) if uid_dict[ask_obj.uid].city_id else ""
    result["ans"]=[]
    for i in all_ans:
        result["ans"].append({"ansid":i.ansid,"ans_content":i.ans_content,"ans_time":i.ans_time,
                              "uid":i.uid,"name":uid_dict[i.uid].get_namecontent(),
                              "img_url": uid_dict[i.uid].get_img_url(),
                            "province":(settings.AREA_BUFF[uid_dict[i.uid].province_id]["shortname"]) if uid_dict[i.uid].province_id else "",
                            "city":(settings.AREA_BUFF[uid_dict[i.uid].city_id]["shortname"]) if uid_dict[i.uid].city_id else "",
                              "good_num":i.good_num})
    return  result





@app_api(login_required=True)
def ask_addans(request):
    '''
    功能说明:
    问吧--给问题提交答案
    参数说明:
    askid 问题id,int,必传
    content 回答内容, 必传,且不能为空字符串

    返回数据说明:

    提交失败:
    {"errorCode":0,"formError":{"askid":"askid必须为数字"},"data":null,"message":"askid必须为数字"}

    提交成功:
    {"errorCode":0,"formError":{},"data":true,"message":""}

    '''
    post_info=request.POST
    askid=post_info.get("askid","")
    content=post_info.get("content","")
    try:
        askid=int(askid)
    except:
        raise FieldError("askid","askid是必传参数,且为int!")
    assert content,FieldError("content","content不能为空!")
    ask_obj = Ask.objects.get(askid=askid)
    ask_obj.add_answer(request.myuser,content)
    return True

@app_api(login_required=True)
def ask_goodans(request):
    '''
    功能说明:
    问吧--给问题的某个答案点赞
    参数书名:
    ansid 回答ID,int,必传
    返回数据说明:
    提交成功:
    {"errorCode":0,"formError":{},"data":1,"message":""}   #data的只代表 点过赞之后,该问题一共被赞的次数.
    提交失败:
    {"errorCode":0,"formError":{"ansid":"ansid必须为int"},"data":null,"message":"askid必须为int"}
    '''
    post_info=request.POST
    ansid=post_info.get("ansid","")
    assert ansid ,FieldError("ansid","ansid不能为空!")
    try:
        ansid=int(ansid)
    except:
        raise FieldError("ansid","ansid必须为int")
    ans=Answer.objects.get(ansid=ansid)
    ans.good_num+=1
    ans.save()
    return  ans.good_num
