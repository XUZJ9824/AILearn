#! /usr/bin/python
# -*- coding:utf-8 -*-
from utils import propertiesutil
import redis
import time
class RedisUtil(object):

    def __init__(self):
        #host,port= propertiesutil.get_redis_config()
        host ="10.16.81.14"
        port = 6380
        self.client=redis.Redis(host=host,port=port)

    #是否存在key
    def exists_key(self,key):
         return self.client.exists(key)

    #添加key
    def add_key(self,key):
        self.client.set(key,int(time.time()))
        self.client.expire(key,7776000)         #保留三个月的key,去重

if __name__ == '__main__':
    redis_util = RedisUtil()
    print(redis_util.exists_key("spiderIp"))