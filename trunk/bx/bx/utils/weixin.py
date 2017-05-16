#coding:utf-8
from collections import  OrderedDict
from .sha1 import sha1

def weixin_check_signature(token,sign,timestamp,nonce):
    """
    
    :param token:
    :param sign: 
    :param timestamp: 
    :param nonce: 
    :return: 
    """
    info=[token,timestamp,nonce]
    info=[str(i) for i in info]
    info.sort()
    return sha1("".join(info))==sign



