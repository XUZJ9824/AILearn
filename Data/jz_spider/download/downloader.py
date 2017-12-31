#! /usr/bin/python
# -*- coding: utf-8 -*-
import pycurl
import urllib
import json
import random
#import StringIO #python2
from io import StringIO #python3
from utils import mysqlutil
from constant import sql
from utils import logutil

class Downloader(object):

    def __init__(self):
        self.proxys =  self.get_proxys(sql.SELECT_PROXY_SQL)
        self.user_agent_dist = self.get_user_agent_dist(sql.SELECT_UA_SQL)
        self.log_util = logutil.LogUtil()
    def download(self,url,http_param,param):
       request = pycurl.Curl()
       http_param = self.set_method(http_param,param)
       try:
           #设置请求方法
           if http_param['method'] == Method.get:
                request.setopt(pycurl.POST, 0)

           elif http_param['method'] == Method.post:
                request.setopt(pycurl.POST, 1)
                request_data = urllib.urlencode(json.loads(http_param['requestData']))
                request.setopt(pycurl.POSTFIELDS, request_data)

           #设置代理
           if http_param['proxyType'] == Proxy.oneself:
                pass
           elif http_param['proxyType']  == Proxy.exclusive:
                proxy = random.choice(self.proxys)
                request.setopt(pycurl.PROXY, '%s://%s:%s' % (proxy['protocol'],proxy['ip'],proxy['port']))
                request.setopt(pycurl.PROXYUSERPWD, '%s:%s' % (proxy['username'],proxy['password']))
           elif http_param['proxyType'] ==Proxy.free:
                proxy = random.choice( self.proxys)
                request.setopt(pycurl.PROXY, '%s://%s:%s' % (proxy['protocol'],proxy['ip'],proxy['port']))

           #设置url
           request.setopt(pycurl.URL, url)

           #设置ua
           user_agents = self.user_agent_dist[http_param['uaPlatformType']]
           user_agent = random.choice(user_agents)
           request.setopt(pycurl.USERAGENT,user_agent)

           #设置cookie
           request.setopt(pycurl.COOKIE,http_param['cookie'])

           #设置其他header参数
           request.setopt(pycurl.HTTPHEADER, http_param['header'])

           #设置连接超时
           request.setopt(pycurl.CONNECTTIMEOUT, HttpRequestParam.timeout)
           request.setopt(pycurl.TIMEOUT, HttpRequestParam.connnect_timeout)

           body = StringIO.StringIO()
           header = StringIO.StringIO()
           request.setopt(pycurl.HEADERFUNCTION, header.write)
           request.setopt(pycurl.WRITEFUNCTION, body.write)
           request.perform()
           response_body = body.getvalue()
           response_header = header.getvalue()
           return response_body,response_header,request.getinfo(request.HTTP_CODE)
       except Exception as ex:
           self.log_util.error(str(ex))


    def get_proxys(self,sql):
        mysql_util = mysqlutil.MySqlUtil()
        result = mysql_util.select(sql)
        return result

    def get_user_agent_dist(self,sql):
        mysql_util = mysqlutil.MySqlUtil()
        result = mysql_util.select(sql)
        ios,web,android= [],[],[]
        for data in result:
            if data['platform_type'] == 'web':
                web.append(data['value'])
            elif data['platform_type'] == 'ios':
                ios.append(data['value'])
            elif data['platform_type'] == 'android':
                android.append(data['value'])
        result = {"ios":ios,"web":web,"android":android}
        return result

    def set_method(self,http_param,param):
        if "method" in param.keys():
            http_param['method'] = param['method']

        return http_param


class Method(object):
    get =0              #get的请求
    post = 1            #post的请求

class Proxy(object):
    oneself = 0        #本机ip
    exclusive = 1      #独享ip
    free =2            #免费ip

class HttpRequestParam(object):
    timeout = 10
    connnect_timeout = 10




