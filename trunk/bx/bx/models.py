#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/10.
# ---------------------------------

from django.db import  models
import time
from django.conf import  global_settings
import  datetime
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

class Consult(models.Model):
    zid=models.AutoField(primary_key=True)
    title=models.CharField(max_length=50,verbose_name="标题")
    type=models.PositiveSmallIntegerField(max_length=1,default=0,verbose_name="类型",
                                          help_text=u" '资讯类型 默认0，1保险百科 2社会案例 3团体规划，4保险新闻 5监管动态 6保险词条',")
    writer=models.CharField(max_length=30)
    _from=models.CharField(max_length=100,db_column="from",default="",blank=True,verbose_name="来源")
    addtime=models.PositiveIntegerField(default=lambda :int(time.time()),verbose_name="创建时间")
    keywords=models.CharField(max_length=100,default="",blank=True,verbose_name="SEO-关键词")
    description=models.CharField(max_length=100,default="",blank=True,verbose_name="SEO-描述")
    content=RichTextUploadingField(verbose_name="内容")
    status=models.PositiveSmallIntegerField(verbose_name="资讯状态",default=1,help_text="1代表正常 其他值代表异常")
    class Meta:
        db_table="bx_consult"
        ordering=["-addtime"]
        verbose_name="资讯"
        verbose_name_plural="所有资讯"

    def __unicode__(self):
        return self.title+"---"+datetime.datetime.fromtimestamp(self.addtime).strftime("%Y-%m-%d")

class Company(models.Model):
    cid=models.AutoField(primary_key=True)
    comname=models.CharField(max_length=100,verbose_name="企业名",unique=True)
    shortname=models.CharField(max_length=100,verbose_name="企业名简写")
    img=models.ImageField(max_length=200,upload_to="company_img",verbose_name="企业图片")
    class Meta:
        db_table="bx_company"
        verbose_name="保险企业"
        verbose_name_plural="所有保险企业"
    def __unicode__(self):
        return  self.comname

class UserType(models.Model):
    id=models.AutoField(primary_key=True)
    type_name=models.CharField(max_length=50,verbose_name="类型名")
    end_age=models.PositiveIntegerField(default=0,verbose_name="结束年龄")
    img=models.ImageField(max_length=200,upload_to="usertype_img",verbose_name="图片")
    class Meta:
        db_table="bx_usertype_tab"
        verbose_name="保险人群"
        verbose_name_plural="所有保险人群"
    def __unicode__(self):
        return self.type_name

class CateType(models.Model):
    id=models.AutoField(primary_key=True)
    type_name=models.CharField(max_length=80,verbose_name="类型名")
    usertype_id=models.ForeignKey(to=UserType,db_column="usertype_id",verbose_name="人群名")
    class Meta:
        db_table="bx_catetype_tab"
        verbose_name="保险类型"
        verbose_name_plural="所有保险类型"
    def __unicode__(self):
        return self.type_name

class Product(models.Model):
    pid=models.AutoField(primary_key=True)
    pro_name=models.CharField(max_length=100,verbose_name="产品名")
    cid=models.PositiveIntegerField(default=0,verbose_name="企业ID")
    bx_type=models.CharField(max_length=30,verbose_name="产品类型")
    min_price=models.IntegerField(verbose_name="最低价格",default=0)
    bx_feature=models.CharField(max_length=300,verbose_name="产品特色")
    insurance_timelimit=models.CharField(max_length=200,verbose_name="保障期限")
    insurance_paytype=models.CharField(max_length=200,verbose_name="缴费方式")
    insurance_agelimit=models.CharField(max_length=200,verbose_name="承保年龄")
    star_age=models.IntegerField(default=0,verbose_name="投保开始年龄")
    end_age=models.IntegerField(default=0,verbose_name="投保结束年龄")
    pro_desc_content=models.TextField(verbose_name="产品内容")
    pro_desc_case=RichTextUploadingField(verbose_name="投保案例")
    pro_desc_reason=RichTextUploadingField(verbose_name="投保理由")
    pro_desc_duty=RichTextUploadingField(verbose_name="责任免除")
    from_url=models.CharField(max_length=200,verbose_name="采集来源",unique=True)
    img=models.ImageField(max_length=200,upload_to="pro_imgs",verbose_name="产品图片")
    meta=models.CharField(max_length=300,verbose_name="额外信息",default="",blank=True)
    addtime=models.IntegerField(default=0,verbose_name="创建时间戳")
    class Meta:
        db_table="bx_product"
        verbose_name="产品"
        verbose_name_plural="所有产品"

    def __unicode__(self):
        return  self.pro_name







