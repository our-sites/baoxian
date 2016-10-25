# coding:utf-8
__author__ = 'zhoukunpeng'
# --------------------------------
# Created by zhoukunpeng  on 2015/12/24.
# ---------------------------------

from django.db import  models

class MyManager(models.Manager):
    #   主要是配置查询时使用的数据库
    def __init__(self,using):
        models.Manager.__init__(self)
        self._db=using