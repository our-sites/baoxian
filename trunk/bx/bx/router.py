#coding:utf-8
__author__ = 'zhoukunpeng'
# --------------------------------
# Created by zhoukunpeng  on 2016/2/26.
# ---------------------------------


class AppRouter(object):
  def db_for_read(self, model, **hints):
    if hasattr(model.objects, '_db'):
      return model.objects._db
    return 'default'

  def db_for_write(self, model, **hints):
    if hasattr(model.objects, '_db'):
      return model.objects._db
    return  'default'


  def allow_relation(self, obj1, obj2, **hints):
    return None

  def allow_syncdb(self, db, model):
    if hasattr(model.objects, '_db'):
      model_db = model.objects._db
    else:
      model_db = 'default'

    if db == model_db:
      return True
    else:
      return False