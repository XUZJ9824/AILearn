#! /usr/bin/python
# -*- coding: utf-8 -*-
import requests
from lxml import etree

def xpath_parse():
    data = requests.get('http://www.cnblogs.com/zhijun/p/http_requests_zhihu_api.html').text
    root = etree.HTML(data)
    print root.xpath('//*[@id="cnblogs_post_body"]/p[1]/text()')[0]
if __name__ == '__main__':
    xpath_parse()