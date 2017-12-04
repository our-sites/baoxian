# coding:utf-8
__author__ = 'zhou'
# --------------------------------
# Created by zhou  on 2017/02/20.
# ---------------------------------
import time
import random
from gcutils.encrypt import md5
from bx.decorators import *
import login
from itertools import groupby
from collections import OrderedDict
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import os

JsonResponse = lambda x: HttpResponse(json.dumps(x), mimetype="application/javascript")
_modules = os.listdir(os.path.dirname(__file__))
__all__ = [i.replace(".py", "") for i in _modules if i.endswith(".py") and (not i.startswith("__"))]
__all__ += ["get_session_key", "api_gateway", "api_document", "meta_test"]

def get_session_key(request):
    key = md5(str(random.random()) + str(time.time()))
    key = aes_encrypt("1" * 16, "bxapp" + key[15:])
    return JsonResponse({"errorCode": 0, "data": key, "message": "success", "formError": {}})


def meta_test(request):
    data = dict(
        [(i, j) for i, j in request.META.items() if isinstance(i, (str, unicode)) and isinstance(j, (str, unicode))])
    return JsonResponse(data)


@csrf_exempt
def api_gateway(request):
    method = request.GET.get("method", "")
    if sys.bxapi_config.get(method):
        return sys.bxapi_config[method](request)
    else:
        return JsonResponse({"errorCode": 404, "data": None, "message": "can not find the method!", "formError": {}})


def api_document(request):
    info = sys.bxapi_config.items()
    # info=[(1,2)]
    info.sort(key=lambda x: x[0])
    result = OrderedDict()
    for module_name, _iter in groupby(info, key=lambda x: ".".join(x[0].split(".")[:-1])):
        result[module_name] = []
        for j in _iter:
            result[module_name].append((j[0], j[1].__doc__ or ""))
    result = result.items()
    return render_to_response("app_api_document.html", locals(), context_instance=RequestContext(request))
