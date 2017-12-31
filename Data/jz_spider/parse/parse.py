#! /usr/bin/python
# -*- coding: utf-8 -*-
import re
import json
from bs4 import BeautifulSoup
from lxml import etree
from utils import logutil
from constant import charset
import sys
import importlib
importlib.reload(sys)
#1. Python 3 与 Python 2 有很大的区别，其中Python 3 系统默认使用的就是utf-8编码。
#2. 所以，对于使用的是Python 3 的情况，就不需要sys.setdefaultencoding("utf-8")这段代码。
#3. 最重要的是，Python 3 的 sys 库里面已经没有 setdefaultencoding() 函数了。
#sys.setdefaultencoding('utf-8')

log_util = logutil.LogUtil()

def handle_parse(data,param):
    try:
        selector = param['selector']
        selectorType = param['selectorType']
        pageType = param['pageType']
        if selectorType == SelectorType.regex:
           regex=RegexParse()

           data = regex.parse(selector,data,pageType)
        elif selectorType== SelectorType.xpath:
            xpath = XpathParse()
            data = xpath.parse(selector,data,pageType)
        elif selectorType ==  SelectorType.json:
            json = JsonParse()
            data = json.parse(selector,data,pageType)
        elif selectorType  ==  SelectorType.css_selector:
            css_selector = CssSelectorParse()
            data = css_selector.parse(selector,data,pageType)
        return data
    except Exception as ex:
        print(ex)
        log_util.error("{parse error : %s }" % str(ex))



class XpathParse(object):

    def parse(self,selector,data,page_type):
        data  = etree.HTML(data)
        data = data.xpath(selector)
        if data:
            if PageType.content_page_type == page_type:
                data = data[0]
            return data


class RegexParse(object):

    def parse(self,selector,data,page_type):
         data = re.findall(selector,data)
         if data:
            if PageType.content_page_type == page_type:
                data = data[0]
                data = self.remove_tag(data)
                data = self.remove_blank(data)
                data = self.replace_str(data)
            return data

    def remove_tag(self,data):
        data = re.sub('<[^>]*>','',data)
        return data

    def remove_blank(self,data):
        data =re.sub('[\\s]{2,}','',data)
        return data

    def replace_str(self,data):
        data =re.sub('&nbsp;',' ',data)
        return data

class CssSelectorParse(object):

    def parse(self,selector,data,page_type):
        soup = BeautifulSoup(data)
        data = soup.select(selector)
        if data:
            if PageType.content_page_type == page_type:
                data = data[0]
            return data

class JsonParse(object):

    def parse(self,selector,data,page_type):
        data = json.loads(data)
        selector_array = selector.split(":")
        if len(selector_array) == JsonKey.one_key:
            self.parse_one_key(selector_array,data)
        elif  len(selector_array) == JsonKey.two_key:
            self.parse_two_key(selector_array,data)
        elif  len(selector_array) == JsonKey.three_key:
            self.parse_three_key(selector_array,data)
        elif  len(selector_array) == JsonKey.four_key:
            self.parse_four_key(selector_array,data)
        elif  len(selector_array) == JsonKey.five_key:
            self.parse_five_key(selector_array,data)

    def parse_one_key(self,selector_array,data):
        data = data[selector_array[0]]
        return data

    def parse_two_key(self,selector_array,data):
        data = data[selector_array[0]][[selector_array[1]]]
        return data

    def parse_three_key(self,selector_array,data):
        data = data[selector_array[0]][[selector_array[1]]][[selector_array[2]]]
        return data

    def parse_four_key(self,selector_array,data):
        data = data[selector_array[0]][[selector_array[1]]][[selector_array[2]]][[selector_array[3]]]
        return data

    def parse_five_key(self,selector_array,data):
        data = data[selector_array[0]][[selector_array[1]]][[selector_array[2]]][[selector_array[3]]][[selector_array[4]]]
        return data



class SelectorType(object):

    regex ='regex'
    xpath ='xpath'
    css_selector = 'css_selector'
    json ='json'

class JsonKey(object):
    one_key = 1
    two_key = 2
    three_key = 3
    four_key = 4
    five_key = 5

class PageType(object):
    list_page_type = 0
    content_page_type = 1
