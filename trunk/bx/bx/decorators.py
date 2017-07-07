#coding:utf-8


from django.http import  HttpResponse
from django.template import  loader
from django.views.decorators.csrf import  csrf_protect
import types
old_get_template=loader.get_template



def mobile_browser_adaptor_by_host(mobile_host,pc_m_tmeplate_dict):
    def _real_decoractor(view):
        #if getattr(view,"_template_monkey_dict",None):
        view._template_monkey_dict=[mobile_host,pc_m_tmeplate_dict]
        #else:
            #view._template_monkey_dict={mobile_host:{pc_template_name:m_template_name}}
        return view
    return  _real_decoractor