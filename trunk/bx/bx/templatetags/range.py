#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/11/1.
# ---------------------------------
from django import  template
register=template.Library()
@register.filter("range")
def _range(value,arg=None):
    if not arg:
        return  range(value)
    else:
        return  range(value,arg)


@register.filter("near")
def near(value,arg):
    return range(value-arg,value+arg +1)