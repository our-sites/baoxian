#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/18.
# ---------------------------------
from django.shortcuts import  render_to_response

def home(request):
    return  render_to_response("ask.html",locals())