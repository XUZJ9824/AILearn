#! /usr/bin/python
# -*- coding: utf-8 -*-

from utils import mysqlutil
from download import downloader
from utils import logutil
from constant import sql
import json
from format import format
from constant import http
from parse import parse
from constant import charset
from utils import rabbitutil
from field import field
from utils import redisutil
from utils import shorturl

class Spider(object):

    def __init__(self,source,config=None):
        self.log_util = logutil.LogUtil()
        self.mysql_util = mysqlutil.MySqlUtil()
        self.http_code = http.HttpCode()
        self.download = downloader.Downloader()
        self.rabbitmq_util = rabbitutil.RabbitMQUtils()
        self.redis_util = redisutil.RedisUtil()
        self.source = source
        self.init_config(self.source)
        if config is not None :
            self.config = config
        self.http_param = self.config['http_param']
        self.list_page_param = self.config['list_page_param']
        self.content_page_param =self.config['content_page_param']
        self.login_param = self.config['login_param']
        self.apply_param =self.config['apply_param']
        self.cancel_param = self.config['cancel_param']

    def init_config(self,source):
        self.citys = self.mysql_util.select(sql.SELECT_CITY_SQL % source)
        self.categorys = self.mysql_util.select(sql.SELECT_CATEGORY_SQL % source)
        self.accouts = self.mysql_util.select(sql.SELECT_ACCOUNT_SQL % source)
        self.config = self.mysql_util.select(sql.SELECT_CONFIG_SQL % source)

    def start(self):
        for city in self.citys:
            for category in self.categorys:
                    content_list = self.list_page(city,category)
                    urls = self.duplicate(city,category,content_list)
                    for url in urls:
                        try:
                            field_map = self.content_page(url)
                            field_map = self.handle_field(self.source,city,category,url,field_map)
                            print(field_map)
                            self.write_queue(json.dumps(field_map))
                            self.redis_util.add_key(shorturl.get_hash_key(url))
                        except Exception as ex:
                            print(ex)

    #列表页
    def list_page(self,city,category):
        content_list = []
        init_page_num = self.list_page_param['initPageNum']
        raise_page_num = self.list_page_param['raisePageNum']
        end_page_num = self.list_page_param['endPageNum']
        try:
            while init_page_num < end_page_num:
                self.page_url = format.list_page_format(city['key'],category['key'],init_page_num,self.list_page_param)
                print(self.page_url)
                body,header,code = self.download.download(self.page_url,self.http_param,self.list_page_param)
                body = body.decode(self.list_page_param['charset']).encode(charset.UTF8)
                if self.http_code.success == code :
                    element_list =  parse.handle_parse(body,self.list_page_param)
                    if len(element_list) > 0 :
                        for element in element_list:
                            content_list.append(element)
                    else:break
                init_page_num += raise_page_num
        except Exception as ex:
            self.log_util.error("list page error : " + str(ex) )
        finally:
            return  content_list

    #去重
    def duplicate(self,city,category,urls):
        content_urls = []
        for url in urls:
            try:
                content_url = format.content_page_format(city['key'],category['key'],url,self.content_page_param)
                if content_url:
                    hash_key = shorturl.get_hash_key(content_url)
                    boolean = self.redis_util.exists_key(hash_key)
                    if boolean is False:
                        content_urls.append(content_url)
            except Exception as ex:
                continue
        return content_urls

    #内容页
    def content_page(self,url):
        body,header,code =  self.download.download(url,self.http_param,self.content_page_param)
        body = body.decode(self.content_page_param['charset']).encode(charset.UTF8)
        fields = self.content_page_param['fields']
        field_map = {}
        for field_dist in fields:
            try:
                field_map[field_dist['name']] = parse.handle_parse(body,field_dist)
            except Exception as ex:
                print(ex)
        return field_map

    #字段处理
    def handle_field(self,source,city,category,url,field_map):
        return field.handle(source,city,category,url,field_map)

    #写入队列
    def write_queue(self,field_map):
        self.rabbitmq_util.produce_data(field_map)

















def main():
    source = '58'
    config = {
        "http_param":{
            "method":0,  #get/post
            "uaPlatformType": "web",
            "cookie":"",
            "header":[],
            "requestData":"",
            "proxyType":0,
        },

        "list_page_param":{
            "listPageUrlFormat":"http://m.58.com/%s/%s/pn%s/",
            "listPageCombineType":1,
            "initPageNum":8,
            "raisePageNum":1,
            "endPageNum":11,
            "pageType":0,
            "selectorType":"xpath",
            "selector":"//ul/li//@infoid",
            "charset":"utf-8",
        },

        "content_page_param":{
            "contentUrlFormat":"http://m.58.com/%s/%s/%sx.shtml",
            "contentUrlCombineType":1,
            "fields":[
                {"name":"salary",
                 "selectorType":"regex",
                 "selector":"<span class=\"pay\">([\s\S]*?)</span>",
                 "pageType":1,
                 },
                {"name":"title",
                 "selectorType":"regex",
                 "selector":"<span id=\"d_title\" class=\"d_title\">([\s\S]*?)</span>",
                 "pageType":1,
                 },

                {"name":"settlement",
                 "selectorType":"regex",
                 "selector":"<span class=\"rijie\">([\s\S]*?)</div>",
                 "pageType":1,
                 },
                {"name":"publish_date",
                 "selectorType":"regex",
                 "selector":"<span>发布：</span><span>([\s\S]*?)</span>",
                 "pageType":1,
                 },
                 {"name":"work_date",
                 "selectorType":"regex",
                 "selector":"<span class=\"attrName\">时间：([\s\S]*?)</li>",
                 "pageType":1,
                 },
                {"name":"work_time",
                 "selectorType":"regex",
                 "selector":"时间：</span>([\s\S]*?)</span>",
                 "pageType":1,
                 },

                {"name":"work_addr",
                 "selectorType":"regex",
                 "selector":"地址：</span><span class=\"attrValue dizhiValue\">([\\s\\S]*?)</span>",
                 "pageType":1,
                 },
                {"name":"phone",
                 "selectorType":"regex",
                 "selector":"phoneno=\"([\s\S]*?)\"",
                 "pageType":1,
                 },
                {"name":"contacts",
                 "selectorType":"regex",
                 "selector":"联系人：</span>([\s\S]*?)</span>",
                 "pageType":1,
                 },
                {"name":"company_name",
                 "selectorType":"regex",
                 "selector":"<h2 class=\"c_tit c_tit_ell\">([\s\S]*?)</h2>",
                 "pageType":1,
                 },
                {"name":"job_desc",
                 "selectorType":"regex",
                 "selector":"<h2>职位简介</h2>([\s\S]*?)<div class=\"more_wrap\">",
                 "pageType":1,
                 }
            ],
            "charset":"utf-8",
        },
            "login_param":{},
            "apply_param":{},
            "cancel_param":{}
    }
    spider = Spider(source,config)
    spider.start()






#启动 
if __name__ == '__main__':
    main()

