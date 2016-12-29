
from django.http import  HttpResponse
from django.shortcuts import  render_to_response
from django.template.context import  RequestContext

def index(request):
    return render_to_response("work_buy_index.html",locals(),context_instance=RequestContext(request))