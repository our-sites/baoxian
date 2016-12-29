#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/11/14.
# ---------------------------------


from django import  template
register=template.Library()
@register.filter("mod")
def int_mod(value,arg):
    return int(value)%int(arg)

