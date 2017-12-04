#coding:utf-8
# write  by  zhou

import upyun
from django.db import  models
import upyun
from django.core.files.storage import Storage,FileSystemStorage
from django.utils.encoding import filepath_to_uri
import urlparse
import time
import  datetime
from django.core.files.base import ContentFile
import random
import time
from django.conf import  settings


class UpyunStorage(Storage):
    "upyun storage"
    BUCKETNAME = settings.UPYUN_BUCKETNAME
    USERNAME = settings.UPYUN_USERNAME
    PASSWORD = settings.UPYUN_PASSWORD
    BASE_URL = settings.UPYUN_BASE_URL
    up = upyun.UpYun(BUCKETNAME, USERNAME, PASSWORD, timeout=30,
                                        endpoint=upyun.ED_AUTO)

    def _save(self, name, content):
        if  name[0] != '/':
            name = "/" + name
        try:
            res = self.up.put(name, content.read(), checksum=False)
            print res
        except Exception as e:
            raise
        return name

    def exists(self, name):
        try:
            self.up.getinfo(name)
        except Exception:
            return False
        return True

    def url(self, name):
        #  兼容旧的本地存储
        if name.startswith("userimgurl") or name.startswith("proxyuser_imgs"):
            return "https://www.bao361.cn"+settings.MEDIA_URL+name
        #  ######
        return self.BASE_URL+filepath_to_uri(name)
    @classmethod
    def simple_upload(cls,full_path_name,file_content):
        try:
            res = cls.up.put(full_path_name, file_content, checksum=False)
            print res
        except Exception as e:
            raise
        return cls.BASE_URL+filepath_to_uri(full_path_name)