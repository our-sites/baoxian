# coding:utf-8
# write  by  zhou
# 三方登录相关 待完成.....
import urllib2
import json
import StringIO
import traceback
from django.core.files.uploadedfile import InMemoryUploadedFile
from threadspider.utils.encrypt import md5
import random
import  urllib

def oauth_qq(appid, token, ip, province_id, city_id,is_proxy):
    """
    QQ三方登录专用,如果成功, 返回一个用户对象, 如果失败返回False
    """
    from ..models import MyUser,UserQqProfile
    if is_proxy:
        is_proxy = 1
    else:
        is_proxy = 0
    try:
        def get_memoryfile_by_url(url):
            """
            @return: InMemoryUploadedFile which can be assigned to ImageField
            """
            content = urllib2.urlopen(url).read()
            thumb_io = StringIO.StringIO()
            thumb_io.write(content)
            # thumb.save(thumb_io, format="JPEG", quality=quality)
            thumb_file = InMemoryUploadedFile(thumb_io, None, md5(content), 'image/jpeg',
                                              thumb_io.len, None)
            return thumb_file

        result = urllib2.urlopen("https://graph.qq.com/oauth2.0/me?access_token=%s&unionid=1" % token).read().strip()[10:-3]
        result = json.loads(result)
        open_id = result["openid"]
        unionid = result["unionid"]
        appid = "%s" % appid
        result = urllib2.urlopen(
            "https://graph.qq.com/user/get_user_info?access_token=%s&oauth_consumer_key=%s&openid=%s" % (
                token, appid, open_id)).read()
        result = json.loads(result)
        qq_img_url = result["figureurl_qq_2"] or result["figureurl_qq_1"] or result["figureurl"] or result[
            "figureurl_2"] or "http://www.bao361.cn/static/imgs/qq-main.png"
        qq_img_obj = get_memoryfile_by_url(qq_img_url)
        sex = 1 if result["gender"] == "男" else 2
        username = md5(open_id)[:16]
        birthday = "1970-01-01"
        real_name = "QQ用户" + result["nickname"]
        _profile=UserQqProfile.objects.filter(qqid=open_id)
        if _profile.count():
            user_info = MyUser.objects.get(uid=_profile[0].uid)
            user= user_info
        else:
            passwd = str(random.randrange(100000, 999999))
            salt = MyUser.make_salt()
            password = MyUser.hashed_password(salt, passwd)
            user = MyUser(username=username, phone=0, salt=salt, password=password, state=1,
                          ip=ip, birthday=birthday, real_name=real_name, imgurl=qq_img_obj, sex=sex,
                          province_id=province_id, city_id=city_id,vqq=1,is_proxy=is_proxy)
            user.save()
            qq_profile=UserQqProfile(uid=user.uid,qqid=open_id,state=1,regip=ip,jsoninfo=json.dumps(result))
            qq_profile.save()
        return user
    except Exception as e:
        traceback.print_exc()
        return False,u"获取QQ信息失败"


def oauth_weibo(appid,app_secret,code,ip,province_id,city_id,is_proxy):
    from ..models import MyUser,UserWeiboProfile
    assert  code
    def get_memoryfile_by_url(url):
        """
        @return: InMemoryUploadedFile which can be assigned to ImageField
        """
        request = urllib2.Request(
            url)
        request.headers[
            "User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.202 Safari/537.36"
        request.headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        request.headers["Accept-Encoding"] = "gzip, deflate"
        request.headers["Progma"] = "no-cache"
        request.headers["Accept-Language"] = "zh-CN,zh;q=0.8,en;q=0.6"
        request.headers["Upgrade-Insecure-Requests"] = "1"
        content=urllib2.urlopen(request).read()
        thumb_io = StringIO.StringIO()
        thumb_io.write(content)
        # thumb.save(thumb_io, format="JPEG", quality=quality)
        thumb_file = InMemoryUploadedFile(thumb_io, None, md5(content), 'image/jpeg',
                                          thumb_io.len, None)
        return thumb_file
    try:
        data = urllib.urlencode({"client_id": appid, "client_secret": app_secret,
                                 "grant_type": "authorization_code", "code": code,
                                 "redirect_uri": "http://www.bao361.cn/get_weibo_token"})
        result = urllib2.urlopen("https://api.weibo.com/oauth2/access_token", data=data).read()
        access_token = json.loads(result)["access_token"]
        uid_info = json.loads(urllib2.urlopen("https://api.weibo.com/oauth2/get_token_info",
                                              data=urllib.urlencode({"access_token": access_token})).read())
        uid = uid_info["uid"]
        uid = str(uid)
        result=json.loads( urllib2.urlopen(
            "https://api.weibo.com/2/users/show.json?access_token=%s&uid=%s" % (access_token, uid)).read().strip())

        qq_img_url =  result["avatar_large"] or  result["avatar_hd"] or   "http://www.bao361.cn/static/imgs/weibo-icon.jpg"
        qq_img_obj = get_memoryfile_by_url(qq_img_url)
        sex = 1  if  result["gender"]!="f" else 2
        username = md5(result["idstr"])[:10]
        birthday = ""
        real_name = "微博用户" + result["screen_name"][:10]
        _profile=UserWeiboProfile.objects.filter(weiboid=uid)
        if _profile.count():
            user_info = MyUser.objects.get(uid=_profile[0].uid)
            user= user_info
        else:
            passwd = str(random.randrange(100000, 999999))
            salt = MyUser.make_salt()
            password = MyUser.hashed_password(salt, passwd)
            user = MyUser(username=username, phone=0, salt=salt, password=password, state=1,
                          ip=ip, birthday=birthday, real_name=real_name, imgurl=qq_img_obj, sex=sex,
                          province_id=province_id, city_id=city_id,vqq=1,is_proxy=is_proxy)
            user.save()
            qq_profile=UserWeiboProfile(uid=user.uid,weiboid=uid,state=1,regip=ip,jsoninfo=json.dumps(result))
            qq_profile.save()
        return user
    except Exception as e :
        traceback.print_exc()
        return  False,u"获取微博信息失败"



def auth_3_weixin():

    pass


def auth_3_taobao():
    pass



