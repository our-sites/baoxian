
from django.shortcuts import  render_to_response
from django.template.context import RenderContext,RequestContext

def get_template_string(request,template_name,vars=None):
    return  render_to_response(template_name,{} if not vars else vars ,context_instance=RequestContext(request) ).content