
from django.template import  loader

old_loader=loader.get_template

class MobileAdaptorMiddleware(object):
    def process_view(self,request, callback, callback_args, callback_kwargs):
        template_config=getattr(callback,"_template_monkey_dict",None)
        host=request.META["HTTP_HOST"]
        def _get_template(template_name):
            if template_config:
                monkey_host,monkey_config=template_config
                if (  monkey_host==host   if not  hasattr(monkey_host,"__call__")  else monkey_host(host) ) and monkey_config.has_key(template_name) :
                    return  old_loader(monkey_config[template_name])
                else:
                    return  old_loader(template_name)
            else:
                return old_loader(template_name)

        loader.get_template=_get_template