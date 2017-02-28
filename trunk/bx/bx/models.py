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
import  re
import  json
import  HTMLParser


def filter_tags(htmlstr):
    s=re.sub("<[^<>]+>",'',htmlstr)
    return s

def replace_charentity(htmlstr):
    htmlstr=htmlstr.replace("&quot;",'"')
    htmlstr=htmlstr.replace("&amp;",'&')
    htmlstr=htmlstr.replace("&lt;",'<')
    htmlstr=htmlstr.replace("&gt;",'>')
    htmlstr=htmlstr.replace("&nbsp;",' ')
    return htmlstr

class Area(models.Model):
    id=models.AutoField(primary_key=True)
    areaname=models.CharField(max_length=50)
    parentid=models.PositiveIntegerField()
    shortname=models.CharField(max_length=50)
    level=models.PositiveIntegerField()
    class Meta:
        db_table='area'


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
    cid=models.IntegerField(default=0,verbose_name="CID")
    good_num=models.IntegerField(default=0,verbose_name="赞次数")
    see_num=models.IntegerField(default=0,verbose_name="浏览次数")
    abstract=models.TextField(default='',verbose_name="摘要")
    # imghandle_tag=models.PositiveIntegerField(default=0)
    class Meta:
        db_table="bx_consult"
        ordering=["-addtime"]
        verbose_name="资讯"
        verbose_name_plural="所有资讯"

    def __unicode__(self):
        return self.title+"---"+datetime.datetime.fromtimestamp(self.addtime).strftime("%Y-%m-%d")
    def get_simple_content(self):
        a=filter_tags(self.content)
        b= replace_charentity(a)
        _=HTMLParser.HTMLParser()
        return  _.unescape(b.strip())
    def get_date(self):
        return datetime.datetime.fromtimestamp(self.addtime).strftime("%Y-%m-%d")

    def get_datetime(self):
        return  datetime.date.fromtimestamp(self.addtime).strftime("%Y-%m-%d %H:%M:%S")

    def get_type(self):
        config={1:"保险百科",2:"社会案例",3:"保险规划",4:"保险新闻",5:"监管动态",6:"保险词条"}
        if self.type in config:
            return config[self.type]
    def simple_title(self):
        if len(self.title)>17:
            return self.title[:17]+".."
        else:
            return self.title

    def simple_seo_k(self):
        return  self.keywords+(".." if len(self.keywords)>9 else '' )

    def simple_seo_d(self):
        return  self.description+(".." if len(self.description)>9 else "")

    def get_status(self):
        if self.status==1:
            return  "正常"
        else:
            return "禁用"
    def get_from(self):
        return  self._from

class Company(models.Model):
    cid=models.AutoField(primary_key=True)
    comname=models.CharField(max_length=100,verbose_name="企业名",unique=True)
    shortname=models.CharField(max_length=100,verbose_name="企业名简写")
    img=models.ImageField(max_length=200,upload_to="company_img",verbose_name="企业图片")
    product_weight=models.IntegerField(default=0)   #权重
    dailiren_weight=models.IntegerField(default=0)    #权重
    content=models.TextField()  #企业介绍
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
    min_price=models.DecimalField(verbose_name="最低价格",default=0.000,max_digits=10,decimal_places=3)
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
        ordering=["-addtime"]

    def __unicode__(self):
        return  self.pro_name

    def get_pro_desc_json(self):
        try:
            return  json.loads(self.pro_desc_content)
        except:
            return []

    def get_type_name_list(self):
        t_list=[]
        for i in self.bx_type.split(","):
            try:
                t_list.append(int(i))
            except:
                pass
        objs=CateType.objects.filter(id__in=t_list)
        return [i.type_name  for i in objs]

    def get_type_id_list(self):
        t_list=[]
        for i in self.bx_type.split(","):
            try:
                t_list.append(int(i))
            except:
                pass
        objs=CateType.objects.filter(id__in=t_list)
        return [i.id   for i in objs]

    def get_comname(self):
        try:
            return Company.objects.get(cid=self.cid).comname
        except:
            return None

    def get_short_comname(self):
        try:
            return Company.objects.get(cid=self.cid).shortname
        except:
            return None

    def get_comobj(self):
        return  Company.objects.get(cid=self.cid)


class ProductImgCache(models.Model):
    id=models.AutoField(primary_key=True)
    img=models.ImageField(max_length=200,upload_to="pro_imgs",verbose_name="产品图片")

    class Meta:
        db_table="bx_product_img_cache"



class Ask(models.Model):
    askid=models.AutoField(primary_key=True)
    ask_title=models.CharField(max_length=255,verbose_name="标题")
    ask_content=models.CharField(max_length=1000,verbose_name="内容")
    uid=models.IntegerField(default=0,verbose_name="提问者ID")
    ask_time=models.IntegerField(default= lambda :int(time.time()),verbose_name="提问时间")
    mark=models.IntegerField(default=0)
    province=models.IntegerField(default=0)
    city=models.IntegerField(default=0)
    state=models.PositiveIntegerField(default=0)  #状态  正常0    其他为异常
    ans_num=models.PositiveIntegerField(default=0)  #回答数
    class Meta:
        db_table="bx_ask"
        verbose_name="提问"
        verbose_name_plural="所有提问"
    def __unicode__(self):
        return  self.ask_title

    def get_date(self):
        "获取日期信息   2016-01-01"
        return datetime.datetime.fromtimestamp(self.ask_time).strftime("%Y-%m-%d")

    def get_date_time(self):
        return  datetime.datetime.fromtimestamp(self.ask_time).strftime("%Y-%m-%d %H:%M:%S")


    def get_answer_count(self):
        "获取回答数"
        return Answer.objects.filter(askid=self.askid).count()

    def get_area_info(self):
        "获取地域信息"
        if self.city:
            _= Area.objects.get(id=self.city)
            _p=Area.objects.get(id=_.parentid)
            return  _p.shortname+_.shortname
        if self.province:
            _=Area.objects.get(id=self.province)
            return _.shortname
        return  ""

    def get_first_ans(self):
        "获取第一个回答"
        try:
            return Answer.objects.filter(askid=self.askid).order_by("ans_time")[0]
        except:
            return None

    def get_last_ans(self):
        "获取最后一个回答"
        try:
            return Answer.objects.filter(askid=self.askid).order_by("-ans_time")[0]
        except:
            return None

    def add_answer(self,user,content):
        assert  user.usertype==2 #必须为代理人账户
        _ = Answer(askid=int(self.askid), ans_content=content, uid=user.uid, parent_ansid=0)
        _.save()
        profile = user.get_profile()
        # if not  profile:
        #     profile=ProxyUserProfile(uid=request.myuser,ans_num=1)
        #     profile.save()
        if profile:
            profile.ans_num += 1
            profile.save()
        self.ans_num+=1
        self.save()
        return  _

    def get_user(self):
        from myauth.models import MyUser
        return MyUser.objects.get(uid=self.uid)

class Answer(models.Model):
    ansid=models.AutoField(primary_key=True)
    askid=models.PositiveIntegerField(default=0,verbose_name="问题ID")
    ans_content=models.CharField(max_length=1000,verbose_name="内容")
    uid=models.IntegerField(default=0,verbose_name="用户ID")
    ans_time=models.PositiveIntegerField(verbose_name="回答时间",default=lambda :int(time.time()))
    parent_ansid=models.PositiveIntegerField(default=0,verbose_name="父回答ID")
    class Meta:
        db_table="bx_answer"
        verbose_name="回答"
        verbose_name_plural="所有回答"


    def get_date(self):
        "获取日期信息   2016-01-01"
        return datetime.datetime.fromtimestamp(self.ans_time).strftime("%Y-%m-%d")

    def get_date_time(self):
        return datetime.datetime.fromtimestamp(self.ans_time).strftime("%Y-%m-%d %H:%M:%S")

    def get_user(self):
        from myauth.models import  MyUser,ProxyUserProfile
        return MyUser.objects.get(uid=self.uid)

    def get_ask(self):
        return  Ask.objects.get(askid=self.askid)

    def get_user_profile(self):
        from myauth.models import  MyUser,ProxyUserProfile
        return ProxyUserProfile.objects.get(uid__uid =self.uid)




class DingZhi(models.Model):
    did=models.AutoField(primary_key=True)
    birth_year=models.IntegerField(default=0)
    birth_month=models.IntegerField(default=0)
    min_price=models.IntegerField(default=0)
    max_price=models.IntegerField(default=0)
    contact=models.CharField(blank=False,default='',max_length=20)
    province=models.IntegerField(default=0)
    city=models.IntegerField(default=0)
    uid=models.IntegerField(default=0)
    addtime=models.IntegerField(default=lambda :int(time.time()))
    start_hour=models.IntegerField(default=0)
    end_hour=models.IntegerField(default=0)
    realname=models.CharField(max_length=50,default='')

    class Meta:
        db_table="bx_dingzhi"

    def get_date_time(self):
        return datetime.datetime.fromtimestamp(self.addtime).strftime("%Y-%m-%d %H:%M:%S")

class AllSiteMsg(models.Model):
    msgid=models.AutoField(primary_key=True)
    message=models.TextField()
    addtime=models.IntegerField(default=lambda:int(time.time()))
    state=models.PositiveIntegerField(default=0)
    url=models.CharField(max_length=200,default='')

    class Meta:
        db_table="bx_allsite_msg"

    def get_date_time(self):
        return datetime.datetime.fromtimestamp(self.addtime).strftime("%Y-%m-%d %H:%M:%S")



