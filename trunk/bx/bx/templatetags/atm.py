# coding:utf-8
__author__ = 'zhoukunpeng'
# --------------------------------
# Created by zhoukunpeng  on 2015/12/23.
# ---------------------------------
import json
import time
import os
import qconf_py
from django.conf import  settings
class AtmFrame(object):
    def __init__(self,path,request):
        #self.conf=json.loads(qconf_py.get_conf(os.path.join(settings.STATICFILES_DIRS[0] ,"..","maps",path.split(":")[0])+".json"))
        self.conf=qconf_py.get_conf(path)
        self.version=self.conf.get("active")
        self.path=path
        self.setting=self.conf.get("settings",None)
        self.maps=self.conf.get("maps",None)
        self.debug=False
        self.debug_domain="127.0.0.1"
        self.timestamp=str(int(time.time()))
        try:
            getinfo=request.GET
            debugparams=getinfo[self.setting["debugParam"]]
            if debugparams:
                self.debug=True
                if debugparams!='true':
                    self.debug_domain=debugparams
            else:
                pass
        except:
            pass

    def get_css(self):
        try:
            if self.debug==True:
                debugport=self.setting["port"]
                return  self.conf["maps"][self.version][self.path]["debug"]["css"].replace("{{host}}",self.debug_domain).replace("{{timestamp}}",int(time.time()))
                #return  '''<link type="text/css" rel="stylesheet" href="//%s:%s/debug?id=%s&type=css&domain=%s/dev&timestamp=%s" />'''%(self.debug_domain,debugport,self.path,self.debug_domain,int(time.time()))
            else:
                return self.conf["maps"][self.version][self.path]["formal"]["css"]
                #domain=self.setting["domain"]

                # _u=[]
                # for i in  self.conf["maps"][self.path]["css"]:
                #     _u.append('''<link type="text/css" rel="stylesheet" href="%s%s" />'''%(domain,i))
                # return  "\n".join(_u)
        except:
            return ''

    def get_js(self):
        try:
            #assert  self.conf["maps"][self.path]["onlyCss"]==False
            if self.debug==True:
                debugport=self.setting["port"]
                return  self.conf["maps"][self.version][self.path]["debug"]["js"].replace("{{host}}",self.debug_domain).replace("{{timestamp}}",int(time.time()))
                #return  '''<link type="text/css" rel="stylesheet" href="//%s:%s/debug?id=%s&type=css&domain=%s/dev&timestamp=%s" />'''%(self.debug_domain,debugport,self.path,self.debug_domain,int(time.time()))
            else:
                return self.conf["maps"][self.version][self.path]["formal"]["js"]
        except:
            return ''

import datetime
from django import  template
register=template.Library()
class AtmJsNode(template.Node):
    def __init__(self,path):
        self.path=path
    def render(self, context):
        try:
            request=context["request"]
            return AtmFrame(self.path,request).get_js()
        except Exception as e :
            return  str(e),"PATH:%s"%self.path


class AtmCssNode(template.Node):
    def __init__(self,path):
        self.path=path
    def render(self, context):
        try:
            request=context["request"]
            return AtmFrame(self.path,request).get_css()
        except Exception as e :
            return  str(e),"PATH:%s"%self.path

@register.tag("atmjs")
def  atmjs_handle(parser,token):
    try:
        tag_name,path=token.split_contents()
    except:
        return ''
    else:
        return AtmJsNode(path)

@register.tag("atmcss")
def atmcss_handle(parser,token):
    try:
        tag_name,path=token.split_contents()
    except:
        return ''
    else:
        return AtmCssNode(path)