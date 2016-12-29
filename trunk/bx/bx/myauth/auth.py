# coding:utf-8
__author__ = 'zhoukunpeng'
# --------------------------------
# Created by zhoukunpeng  on 2015/12/26.
# ---------------------------------

from  models import  MyUser

class  MyBackend:
    supports_inactive_user=False     # dont   allow  user that have logout !
    def   authenticate(self,username,password):
        try:
            user=MyUser.objects.get(username=username)
            assert   user.check_password(password)==True
        except Exception as e :
            print "Exception",e
            return None
        else:
            return  user

    def get_user(self,user_id):
        try:
            return  MyUser.objects.get(id=int(user_id))
        except:
            return  None
