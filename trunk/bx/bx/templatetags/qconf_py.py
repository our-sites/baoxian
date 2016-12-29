#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/27.
# ---------------------------------
from django.conf import  settings
import os
import  json

def get_conf(path):
    file_path=os.path.join(settings.STATICFILES_DIRS[0],"..","maps",path.split(":")[0],"main.json")
    fl=open(file_path,"r")
    data=fl.read()
    data=json.loads(data)
    return  data