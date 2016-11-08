#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/28.
# ---------------------------------
import  numpy
import  Image
import os
allfiles=os.listdir("proxyuser_imgs")
for i in allfiles:
    a=Image.open("./proxyuser_imgs/%s"%i)
    b=a.crop((272,0,640,368))
    b.save("./proxyuser_imgs_1/%s"%i,"JPEG")