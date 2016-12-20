from pypinyin import  pinyin
import  pypinyin

from django import  template
register=template.Library()


@register.filter("first_letter")
def _(string):
    if isinstance(string,unicode):
        pass
    else:
        string=string.decode("utf-8")
    return  pinyin(string,style=pypinyin.FIRST_LETTER)[0][0]