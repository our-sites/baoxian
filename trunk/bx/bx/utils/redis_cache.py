#coding:utf-8
# write  by  zhou


import redis
from django.conf import settings
conn = redis.Redis(
                    connection_pool=redis.ConnectionPool(max_connections=4,**settings.REDIS))
def cache_set(key,value,expires=None):
    return conn.set(key,value,expires)

def cache_get(key):
    return conn.get(key)

def cache_ttl(key):
    return conn.ttl(key)

def cache_del(key):
    return conn.delete(key)

def cache_get_raw_conn():
    return conn