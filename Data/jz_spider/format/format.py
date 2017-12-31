#! /usr/bin/python
# -*- coding: utf-8 -*-

from utils import logutil

log_util = logutil.LogUtil()

def list_page_format(city,category,page ,list_page_param):
   try:
        global page_url
        if list_page_param['listPageCombineType'] == ListPageFormat.city_category_page:
            page_url = list_page_param['listPageUrlFormat'] % (city,category,page)
        elif list_page_param['list_page_combine_type'] == ListPageFormat.city__page:
            page_url = list_page_param['listPageUrlFormat'] % (city,page)
        elif list_page_param['list_page_combine_type'] == ListPageFormat.category__page:
            page_url = list_page_param['listPageUrlFormat'] % (category,page)
        elif list_page_param['list_page_combine_type'] == ListPageFormat.page:
            page_url = list_page_param['listPageUrlFormat'] % (page)
        return page_url
   except Exception as ex:
       log_util.error("format error : %s " % str(ex))


def content_page_format(city,category,url ,content_page_param):
    try:
        global content_url
        if content_page_param['contentUrlCombineType'] == ContentPageFormat.city_category_detail:
            content_url = content_page_param['contentUrlFormat'] % (city,category,url)
        elif content_page_param['contentUrlCombineType'] == ContentPageFormat.city_detail:
            content_url = content_page_param['contentUrlFormat'] % (city,url)
        elif content_page_param['contentUrlCombineType'] == ContentPageFormat.category_detail:
            content_url = content_page_param['contentUrlFormat'] % (category,url)
        elif content_page_param['contentUrlCombineType'] == ContentPageFormat.detail:
            content_url = content_page_param['contentUrlFormat'] % (url)
        return content_url
    except Exception as ex:
        log_util.error("format error : %s " % str(ex))



class ListPageFormat(object):
    city_category_page = 1
    city__page = 2
    category__page = 3
    page = 4


class ContentPageFormat(object):
    city_category_detail =1
    city_detail =2
    category_detail =3
    detail =4
