#coding:utf-8
# write  by  zhou

class AppCrosMiddleware(object):
    def process_response(self,request,response):
        if request.META.get("HTTP_HOST","")=="app.bao361.cn":
            if request.META.get("HTTP_ORIGIN",""):
                response["Access-Control-Allow-Origin"] = request.META.get("HTTP_ORIGIN")
        return  response