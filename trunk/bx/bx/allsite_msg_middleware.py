#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/31.
# ---------------------------------

from models import AllSiteMsg


class AllSiteMsgMiddleware(object):
    def process_request(self, request):
        def send_allsite_msg(msg,url=None):
            msg_object=AllSiteMsg(message=msg,url=url  if url else ''  )
            msg_object.save()
            return  msg_object
        request.send_allsite_msg=send_allsite_msg
        request.get_allsite_msg=AllSiteMsg.objects.filter(state=0).order_by("-addtime")
        print "proces_allsite_msg"

