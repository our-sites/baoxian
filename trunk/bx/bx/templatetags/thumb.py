
from django import  template
register=template.Library()


@register.filter("thumb_img")
def thumb_img(value,size_string):
    if value and value[-4:] in (".jpg",".png"):
        return  value+"-"+size_string+value[-4:]
    if value[-5:] ==".jpeg":
        return  value+"-"+size_string+".jpeg"
    return value
