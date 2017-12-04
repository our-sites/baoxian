#coding:utf-8
__author__ = 'zhoukunpeng'
# --------------------------------
# Created by zhoukunpeng  on 2016/7/19.
# ---------------------------------
#coding:utf-8
__author__ = 'zhoukunpeng'
# --------------------------------
# Created by zhoukunpeng  on 2016/7/13.
# ---------------------------------
import base64
from   CryptoPlus.Cipher import   python_Rijndael
from urllib import  unquote
import  random
def cookie_decode(text,key):
    text=base64.b64decode(text)
    if len(key)<=16:
        key=key+(16-len(key))*"\0"
    elif len(key)<=24:
        key=key+(24-len(key))*'\0'
    elif len(key)<=32:
        key=key+(32-len(key))*'\0'
    obj=python_Rijndael.new(key,python_Rijndael.MODE_CBC,IV=text[:32],blocksize=32)
    text=obj.decrypt(text[32:])
    return  text.strip("\x00")

def cookie_encode(text,key):
    if len(key)<=16:
        key=key+(16-len(key))*"\0"
    elif len(key)<=24:
        key=key+(24-len(key))*'\0'
    elif len(key)<=32:
        key=key+(32-len(key))*'\0'
    if len(text)<=32:
        text+="\0"*(32-len(text))
    elif len(text)<=64:
        text+="\0"*(64-len(text))
    elif len(text)<=96:
        text+="\0"*(96-len(text))
    obj=python_Rijndael.new(key,python_Rijndael.MODE_CBC,IV="".join(random.sample("abcdefghigklmnopqrstuvwxyz"*2,32)),blocksize=32)
    text=obj.encrypt(text)
    return  base64.b64encode(obj.IV+text)

def  phpcookie_decode(text,key):
    try:
        return cookie_decode(unquote(text),key)
    except:
        return ''
def phpcookie_encode(text,key):
    if isinstance(text,unicode):
        text = text.encode("utf-8")
    return  cookie_encode(text,key)

if __name__ == "__main__":
    import sys
    text = u'3063\tweixin\u7528\u6237Od\t0.0.0.0\t1511437646'
    key	= 'gc895316'
    print phpcookie_encode(text,key)




