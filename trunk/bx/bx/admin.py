#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/10.
# ---------------------------------

from django.contrib import  admin
from models import Consult,Company,UserType,CateType,Product
admin.site.register([Consult,Company,UserType,CateType,Product])