#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/11.
# ---------------------------------
from django.db import  models

class Area(models.Model):
    id=models.AutoField(primary_key=True)
    areaname=models.CharField(max_length=50)
    parentid=models.IntegerField()
    shortname=models.CharField(max_length=50)
    level=models.IntegerField()
    class Meta:
        db_table="area"