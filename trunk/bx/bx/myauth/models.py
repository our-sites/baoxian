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
   # weixin=models.CharField(max_length=100)  # weixin vchar(100) 微信号
    imgurl=models.ImageField(max_length=100,upload_to="userimgurl")  # imgurl vchar(100)    头像url
    sex=models.PositiveSmallIntegerField(default=0)  # sex tinyint(1) unsigned     性别  1男  2女
    birthday=models.CharField(default="",max_length=30)  # birthday int(11) unsigned   生日  20160101
    ip=models.CharField(max_length=15)  # ip vchar(15)   注册IP
    usertype=models.PositiveSmallIntegerField(default=0)  # usertype tinyint(1) unsigned   用户类型  1 投保人  2 代理人
    addtime=models.PositiveIntegerField(default=lambda:int(time.time()))  #创建时间
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
            return False

    @classmethod
    def make_salt(cls):
        _u=random.sample(["a","b","c","d","e","f","0","1","2","3","4","5","6","7"],6)
        return "".join(_u)

    def __unicode__(self):
        return  self.username

    class Meta:
        db_table="bx_user"

    def get_profile(self):
        if self.usertype==1:
            try:
                return BuyUserProfile.objects.get(uid__uid=self.uid)
            except:
                return None
        elif self.usertype==2:
            try:
                return  ProxyUserProfile.objects.get(uid__uid=self.uid)
            except:
                return None
        else:
            return    None

class ProxyUserProfile(models.Model):
    id=models.AutoField(primary_key=True)
    position=models.CharField(max_length=100,default='')
    cid=models.IntegerField(default=0)
    weixin=models.CharField(max_length=100)
    my_ad=models.TextField()
    uid=models.ForeignKey(to=MyUser,db_column="uid")
    certifi_num=models.CharField(max_length=50,unique=True) #资格证编号
    certifi_status=models.IntegerField(default=0)   #1 待审核  2 审核通过  3 拘审
    certifi_message=models.CharField(max_length=50)
    practice_num=models.CharField(max_length=50)      #执业证编号
    province=models.IntegerField(default=0)
    city=models.IntegerField(default=0)
    zone=models.IntegerField(default=0)
    class Meta:
        db_table="bx_proxyuser_profile"

    def get_user(self):
        return self.uid

    def get_city_info(self):
        try:
            return Area.objects.get(id=self.city).shortname
        except:
            return  ''
    def get_comname(self):
        try:
            return Company.objects.get(cid=self.cid).comname
        except:
            return ""

class BuyUserProfile(models.Model):
    id=models.AutoField(primary_key=True)
    uid=models.ForeignKey(to=MyUser,db_column="uid")
    province=models.IntegerField(default=0)
    city=models.IntegerField(default=0)
    zone=models.IntegerField(default=0)
    class Meta:
        db_table="bx_buyuser_profile"




