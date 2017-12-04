#coding:utf-8


from django.http import  HttpResponse
from django.template import  loader
from django.views.decorators.csrf import  csrf_protect,csrf_exempt
import  sys
import types
old_get_template=loader.get_template
import  json
from utils.redis_cache import *
from utils.aes import *
from myauth.models import MyUser
import traceback
from django.utils.importlib import import_module
from django.conf import  settings
import time
from threadspider.utils.encrypt import md5


JsonResponse=lambda x:HttpResponse(json.dumps(x,indent=True),mimetype="application/javascript")

def mobile_browser_adaptor_by_host(mobile_host,pc_m_tmeplate_dict):
    def _real_decoractor(view):
        #if getattr(view,"_template_monkey_dict",None):
        view._template_monkey_dict=[mobile_host,pc_m_tmeplate_dict]
        #else:
            #view._template_monkey_dict={mobile_host:{pc_template_name:m_template_name}}
        return view
    return  _real_decoractor




class FieldError(Exception):
    def __init__(self,field_name,message):
        Exception.__init__(self)
        self.message=message
        self.field_name=field_name

    def __str__(self):
        return str("$fielderror"+json.dumps({"field_name":self.field_name,"message":self.message}))

    def __unicode__(self):
        return unicode("$fielderror"+json.dumps({"field_name":self.field_name,"message":self.message}))

class ReturnValue(Exception):
    def __init__(self,data,message=""):
        self.data=data
        self.message=message

def app_api(login_required=False):
    def _app_api(views):
        @csrf_exempt
        def _(request,*args,**kwargs):

            session_info=request.META.get("HTTP_SESSION","")
            try:
                assert  session_info
                assert aes_decrypt('1'*16,session_info).startswith("bxapp")
            except:
                _result= JsonResponse({"errorCode":403,"message":"you have no permission to this api","formError":{},"data":None})
            else:
                engine = import_module("bx.app.session_engine.db")
                request.appsession=engine.SessionStore(md5(session_info))
                try:
                    value=request.appsession.get("uid")
                    uid=int(value)
                    user=MyUser.objects.get(uid=uid,state=1,is_proxy=1)
                    assert  user.app_session_info ==session_info
                    request.myuser=user
                except:
                    request.myuser=None

                if login_required and request.myuser==None:
                        _result= JsonResponse({"errorCode":403,"message":"you have no permission to this api","formError":{},"data":None})
                else:
                    try:
                        try:
                            result=views(request,*args,**kwargs)
                        except AssertionError as _re:
                            if str(_re).startswith("$fielderror"):
                                _re_info=str(_re).strip("$fielderror")
                                _re_info=json.loads(_re_info)
                                raise FieldError(_re_info["field_name"],_re_info["message"])
                    except  FieldError as e :
                        _result= JsonResponse({"errorCode":0,"message":e.message,"formError":
                            {"name":e.field_name,"message":e.message},"data":None})
                    except Exception as e :
                        traceback.print_exc()
                        _result= JsonResponse({"errorCode":500,"message":str(e),"formError":
                            {},"data":None})
                    else:
                        message=""
                        if isinstance(result,ReturnValue):
                            message=result.message
                            result=result.data
                        _result= JsonResponse({"errorCode":0,"message":message,"formError":{},"data":result})
                    try:
                        modified = request.appsession.modified
                        empty = request.appsession.is_empty()
                    except AttributeError:
                        pass
                    else:
                        # First check if we need to delete this cookie.
                        # The session should be deleted only if the session is entirely empty
                        print modified,empty
                        if (modified or settings.SESSION_SAVE_EVERY_REQUEST) and not empty:
                            print "save....."
                            request.appsession.save()
            print "[APPAPI_RESULT]:",_result.content
            return _result
        _.__doc__=views.__doc__
        if not getattr(sys,"bxapi_config",None):
            sys.bxapi_config={}
        sys.bxapi_config[views.__module__+"."+views.__name__]=_
        return _
    return _app_api

