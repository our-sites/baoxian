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
    birthday=models.IntegerField(default=0)  # birthday int(11) unsigned   生日  20160101
    ip=models.CharField(max_length=15)  # ip vchar(15)   注册IP
    province=models.PositiveIntegerField(default=0)  # province int(11) unsigned      省id
    city=models.PositiveIntegerField(default=0)  # city int(11) unsigned     市id
    zone=models.PositiveIntegerField(default=0)  # zone int(11) unsigned     区id
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

    def hashed_password(self,password=None):
        if not password:
            return  self.password
        else:
            return   md5(md5(password+self.salt))

    def check_password(self,password):
        if  self.state==1 and   self.hashed_password(password)==self.password:
            return True
        else:
            return False
    def make_salt(self,password):
        _u=random.sample(["a","b","c","d","e","f","0","1","2","3","4","5","6","7"],6)
        return "".join(_u)
    def __unicode__(self):
        return  self.username

    class Meta:
        db_table="bx_user"

