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
from utils import  seo
import pyquery
import jieba.posseg as pseg
from storages import UpyunStorage

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
    _from=models.CharField(max_length=100,db_column="from",default="",blank=True,verbose_name="来源",unique=True)
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

    def get_type_url(self):
        config={1:"/zixun/baike/",2:"/zixun/anli/",3:"/zixun/guahua/",
                4:"/zixun/xinwen/",5:"/zixun/dongtai/",6:"/zixun/citiao/"}
        return  config[self.type]

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

    def get_content_imgs(self):
        _=pyquery.PyQuery("<div>"+self.content+"</div>")
        return [  pyquery.PyQuery(i).attr("src")  for i in   _("img[src^='/media/']")]


class News(models.Model):
    nid=models.AutoField(primary_key=True)
    title=models.CharField(max_length=50,verbose_name="标题")
    cate1=models.PositiveSmallIntegerField(default=0)
    cate2=models.PositiveIntegerField(default=0)
    writer=models.CharField(max_length=30)
    _from=models.CharField(max_length=100,db_column="from",default="",blank=True,verbose_name="来源",unique=True)
    addtime=models.PositiveIntegerField(default=lambda :int(time.time()),verbose_name="创建时间")
    keywords=models.CharField(max_length=100,default="",blank=True,verbose_name="SEO-关键词")
    description=models.CharField(max_length=100,default="",blank=True,verbose_name="SEO-描述")
    tags=models.CharField(max_length=100,default='',verbose_name="标签")
    content=RichTextUploadingField(verbose_name="内容")
    status=models.PositiveSmallIntegerField(verbose_name="资讯状态",default=1,help_text="1代表正常 其他值代表异常")
    cid=models.IntegerField(default=0,verbose_name="CID")
    good_num=models.IntegerField(default=0,verbose_name="赞次数")
    see_num=models.IntegerField(default=0,verbose_name="浏览次数")
    abstract=models.TextField(default='',verbose_name="摘要")

    class Meta:
        db_table="bx_news"
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

    def get_datetimeinfo_before_content(self):
        obj=datetime.datetime.fromtimestamp(self.addtime)
        now=datetime.datetime.now()
        delta=now-obj
        onehour=datetime.timedelta(minutes=60)
        oneday=datetime.timedelta(days=1)
        if delta.total_seconds() <3600:
            return "%s分钟前"%int(delta.total_seconds()/60)
        if delta.total_seconds()<86400:
            return "%s小时前"%(int(delta.total_seconds()/3600))
        return self.get_date()

    def get_tags(self):
        tags=re.sub("[\s+\.\!\/_$%^*(+\"\']+|[+——！，“：“。？、~@#￥%……&*（）]+".decode("utf8"), "",self.tags)
        _=tags.split(",")
        return [ i  for i in _ if i.strip()!=""][:3]

    def get_cate1(self):
        return NewsCate.objects.get(cateid=self.cate1)

    def get_cate1_url(self):
        return "/news/%s/"%(self.cate1)

    def get_cate2_url(self):
        return "/news/%s/"%(self.cate2)

    def get_cate2(self):
        return NewsCate.objects.get(cateid=self.cate2)



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

    def get_content_imgs(self):
        _=pyquery.PyQuery("<div>"+self.content+"</div>")
        return [  pyquery.PyQuery(i).attr("src")  for i in   _("img[src]")]


class NewsCate(models.Model):
    '新闻分类model'
    cateid=models.AutoField(primary_key=True)
    catename=models.CharField(max_length=200)
    parentid=models.PositiveIntegerField(default=0)
    level=models.PositiveIntegerField(default=0)
    class Meta:
        db_table="bx_news_cate"
        verbose_name="新闻分类"
        verbose_name_plural="所有新闻分类"
    def get_url(self):
        return "/news/{0}/".format(self.cateid)

    def get_childrens(self):
        if self.level==1:
            return  NewsCate.objects.filter(parentid=self.cateid)
        else:
            return []


class Company(models.Model):
    cid=models.AutoField(primary_key=True)
    comname=models.CharField(max_length=100,verbose_name="企业名",unique=True)
    shortname=models.CharField(max_length=100,verbose_name="企业名简写")
    img=models.ImageField(max_length=200,upload_to="/media/company_img",verbose_name="企业图片",storage=UpyunStorage())
    product_weight=models.IntegerField(default=0)   #权重
    dailiren_weight=models.IntegerField(default=0)    #权重
    content=models.TextField()  #企业介绍
    video_url=models.CharField(max_length=500,default='')
    class Meta:
        db_table="bx_company"
        verbose_name="保险企业"
        verbose_name_plural="所有保险企业"
    def __unicode__(self):
        return  self.comname

    def get_video_id(self):
        if not  self.video_url:
            return None
        else:
            return re.search(r"id_(.+)\.html",self.video_url).groups()[0]

class UserType(models.Model):
    id=models.AutoField(primary_key=True)
    type_name=models.CharField(max_length=50,verbose_name="类型名")
    end_age=models.PositiveIntegerField(default=0,verbose_name="结束年龄")
    img=models.ImageField(max_length=200,upload_to="/media/usertype_img",verbose_name="图片",storage=UpyunStorage())
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
    img=models.ImageField(max_length=200,upload_to="/media/pro_imgs",verbose_name="产品图片",storage=UpyunStorage())
    meta=models.CharField(max_length=300,verbose_name="额外信息",default="",blank=True)
    addtime=models.IntegerField(default=0,verbose_name="创建时间戳")
    keywords=models.CharField(default="",max_length=100)
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

    def get_keywords(self):
        return self.keywords or self.pro_name


class ProductImgCache(models.Model):
    id=models.AutoField(primary_key=True)
    img=models.ImageField(max_length=200,upload_to="/media/pro_imgs",verbose_name="产品图片",storage=UpyunStorage())

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
    keywords=models.CharField(max_length=200,default='')
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
        return self.ans_num

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
        #assert  user.usertype==2 #必须为代理人账户
        _ = Answer(askid=int(self.askid), ans_content=content, uid=user.uid, parent_ansid=0)
        _.save()

        # if not  profile:
        #     profile=ProxyUserProfile(uid=request.myuser,ans_num=1)
        #     profile.save()
        user.ans_num += 1
        user.save()
        self.ans_num+=1
        self.save()
        return  _

    def get_user(self):
        from myauth.models import MyUser
        return MyUser.objects.get(uid=self.uid)

    def save(self, force_insert=False, force_update=False, using=None):
        models.Model.save(self,force_insert,force_update,using)


    def get_keywords(self):
        if self.keywords:
            return self.keywords
        else:
            return  self.ask_content



class Answer(models.Model):
    ansid=models.AutoField(primary_key=True)
    askid=models.PositiveIntegerField(default=0,verbose_name="问题ID")
    ans_content=models.CharField(max_length=1000,verbose_name="内容")
    uid=models.IntegerField(default=0,verbose_name="用户ID")
    ans_time=models.PositiveIntegerField(verbose_name="回答时间",default=lambda :int(time.time()))
    parent_ansid=models.PositiveIntegerField(default=0,verbose_name="父回答ID")
    good_num=models.PositiveIntegerField(default=0,verbose_name="被赞次数")
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
        from myauth.models import  MyUser
        return MyUser.objects.get(uid=self.uid)

    def get_ask(self):
        return  Ask.objects.get(askid=self.askid)


    def save(self, force_insert=False, force_update=False, using=None):
        models.Model.save(self,force_insert,force_update,using)
        seo.postBaiDu("http://www.bao361.cn/ask/detail/%s.html"%self.get_ask().askid)




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
    ip=models.CharField(max_length=15,default='')
    url=models.CharField(max_length=200,default='')


    class Meta:
        db_table="bx_dingzhi"

    def get_date(self):
        return  datetime.datetime.fromtimestamp(self.addtime).strftime("%Y-%m-%d")

    def get_date_time(self):
        return datetime.datetime.fromtimestamp(self.addtime).strftime("%Y-%m-%d %H:%M:%S")

    def save(self, force_insert=False, force_update=False, using=None):
        result=models.Model.save(self,force_insert,force_update,using)
        from utils import  sms
        sms.send_dingzhi_addsuccess(self.contact)
        return  result

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



class Share(models.Model):
    "签单分享"
    sid=models.AutoField(primary_key=True)
    title=models.CharField(max_length=200,default='')
    addtime=models.PositiveIntegerField(default=lambda:int(time.time()))
    uptime=models.PositiveIntegerField(default=lambda :int(time.time()))
    cid=models.PositiveIntegerField(default=0)
    pid=models.PositiveIntegerField(default=0)
    other_proname=models.CharField(max_length=200,default='')
    content=models.TextField()
    price=models.PositiveIntegerField(default=0)
    uid=models.PositiveIntegerField(default=0)

    class Meta:
        db_table="bx_share"

    def get_date_time(self):
        return datetime.datetime.fromtimestamp(self.uptime).strftime("%Y-%m-%d %H:%M:%S")

    def get_comobj(self):
        return  Company.objects.get(cid=self.cid)

    def get_simple_content(self):
        a=filter_tags(self.content)
        b= replace_charentity(a)
        _=HTMLParser.HTMLParser()
        return  _.unescape(b.strip())

    def get_date(self):
        return datetime.datetime.fromtimestamp(self.uptime).strftime("%Y-%m-%d")




class AddPosition(models.Model):
    '职位'
    apid=models.AutoField(primary_key=True)
    info=models.CharField(max_length=50)

    class Meta:
        db_table="bx_add_position"
        ordering=["apid"]




class AddMoney(models.Model):
    "薪资"
    amid=models.AutoField(primary_key=True)
    info=models.CharField(max_length=50)

    class Meta:
        db_table="bx_add_money"
        ordering=["amid"]


class AddDegree(models.Model):
    "学位"
    adid=models.AutoField(primary_key=True)
    info=models.CharField(max_length=50)

    class Meta:
        db_table="bx_add_degree"
        ordering=["adid"]






class Add(models.Model):
    "增员 model"
    aid=models.AutoField(primary_key=True)
    uid=models.PositiveIntegerField(default=0)
    title=models.CharField(max_length=100,default='') # title
    apid=models.PositiveIntegerField(default=0) # position
    amid=models.PositiveIntegerField(default=0) # money
    adid=models.PositiveIntegerField(default=0) # degree
    cid=models.PositiveIntegerField(default=0)
    work_year=models.PositiveIntegerField(default=0)  # work year
    num=models.PositiveIntegerField(default=0)  # peopele num
    need_content=models.TextField()     # need description
    work_content=models.TextField()     # work description
    phone=models.CharField(max_length=30) # phone info
    address=models.CharField(max_length=30)  # work address
    addtime=models.IntegerField(default=lambda :int(time.time()))
    uptime=models.IntegerField(default=lambda:int(time.time()))

    class Meta:
        db_table="bx_add"

    def get_simple_need_content(self):
        a=filter_tags(self.need_content)
        b= replace_charentity(a)
        _=HTMLParser.HTMLParser()
        return  _.unescape(b.strip())

    def get_simple_work_content(self):
        a=filter_tags(self.work_content)
        b= replace_charentity(a)
        _=HTMLParser.HTMLParser()
        return  _.unescape(b.strip())

    def get_date_time(self):
        return datetime.datetime.fromtimestamp(self.uptime).strftime("%Y-%m-%d %H:%M:%S")

    def get_date(self):
        return datetime.datetime.fromtimestamp(self.uptime).strftime("%Y-%m-%d")



class Advice(models.Model):
    "咨询,一般指一对一咨询 "
    iid = models.AutoField(primary_key=True)
    uid = models.PositiveIntegerField(default=0)  #uid为 0代表非登录用户   uid>0 代表是已登录用户
    name = models.CharField(max_length=20,default='')
    phone = models.PositiveIntegerField(default=0)
    content = models.CharField(max_length=300,default='')
    addtime = models.PositiveIntegerField(default=lambda:int(time.time()))
    ip = models.CharField(max_length=50,default='')
    province_id = models.PositiveIntegerField(default=0)
    city_id = models.PositiveIntegerField(default=0)
    touid = models.PositiveIntegerField(default=0,db_column="to_uid")
    is_replyed = models.PositiveSmallIntegerField(default=0)  #是否已回复   1 已回复 0未回复

    class Meta:
        db_table="bx_advice"

    def get_date_time(self):
        return  datetime.datetime.fromtimestamp(self.addtime).strftime("%Y%m%d %H:%M:%S")

    def send_success_add_sms(self):
        "发送创建成功短信"
        from utils import  sms
        from myauth.models import MyUser
        sms.send_advice_addsuccess(self.phone)
        try:
            assert  self.touid
            _user=MyUser.objects.get(uid=self.touid)
        except:
            pass
        else:
            sms.send_advice_received(str(_user.phone),str(self.phone))

    def add_reply(self,content):
        _ = AdviceReply(iid=self.iid,uid=self.touid,touid=self.uid,content=content)
        _.save()
        self.is_replyed = 1
        self.save()
        return True

    def get_by_user(self):
        from myauth.models import MyUser
        if self.uid:
            return MyUser.objects.get(uid=self.uid)
        else:
            return None


class AdviceReply(models.Model):
    "咨询的回复"
    id = models.AutoField(primary_key=True)
    iid = models.PositiveIntegerField(default=0)
    uid = models.PositiveIntegerField(default=0)
    touid = models.PositiveIntegerField(default=0)
    content = models.TextField(default='')
    addtime = models.PositiveIntegerField(default=lambda:int(time.time()))

    class Meta:
        db_table = "bx_advice_reply"

# class Statis(models.Model):
#     sid=models.AutoField(primary_key=True)
#     uid=models.PositiveIntegerField(default=0)


class StudyVideo(models.Model):
    "视频"
    vid=models.AutoField(primary_key=True)
    video_type=models.PositiveSmallIntegerField(default=0)  # 1 代表新手  2代表签单  3代表增员
    video_source=models.PositiveSmallIntegerField(default=0) # 1 代表 youku
    title=models.CharField(max_length=50,default="")
    addtime=models.PositiveIntegerField(default=lambda:int(time.time()))
    video_id=models.CharField(max_length=100,default="")
    author=models.CharField(max_length=100,default='')
    author_imgurl=models.CharField(max_length=300,default="")
    video_imgurl=models.CharField(max_length=300,default="")
    duration=models.PositiveIntegerField(default=0) #时长
    good_num=models.PositiveIntegerField(default=0)
    play_num=models.PositiveIntegerField(default=0)
    comment_num=models.PositiveIntegerField(default=0)
    class Meta:
        db_table="bx_study_video"

    def get_video_source(self):
        config={1:"youku"}
        return  config[self.video_source]

    def get_video_type(self):
        config={1:"新手",2:"签单",3:"增员"}
        return config[self.video_type]

    def add_comment(self,user,content):
        uid=user.uid
        _=StudyVideoComment(vid=self.vid,content=content,uid=uid)
        _.save()
        self.comment_num+=1
        self.save()
        return  _

class StudyVideoComment(models.Model):
    "视频评论"
    id=models.AutoField(primary_key=True)
    vid=models.PositiveIntegerField(default=0)
    parentid=models.PositiveIntegerField(default=0) #父id
    pparentid=models.PositiveIntegerField(default=0) #祖先id
    content=models.CharField(max_length=300,default="")
    addtime=models.PositiveIntegerField(default= lambda:int(time.time()))
    uid=models.PositiveIntegerField(default=0)
    good_num=models.PositiveIntegerField(default=0)
    class Meta:
        db_table = "bx_study_video_comment"




