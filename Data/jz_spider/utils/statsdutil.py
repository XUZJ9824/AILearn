#! /usr/bin/python
# -*- coding:utf-8 -*-
import statsd
import propertiesutil
class StatsdUtils(object):

    def __init__(self):
        host,port,prefix= propertiesutil.get_statsd_config()
        self.client = statsd.StatsClient(host, port, prefix=prefix);

    def count(self,name,num):
        self.client.incr(name,num)

    def time(self,name,times):
        self.client.timer(name,times)
