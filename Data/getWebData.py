__author__ = 'CQC'
# -*- coding:utf-8 -*-

import urllib
import urllib3
import re


class Spider:
    def __init__(self):
        self.siteURL = 'http://mm.taobao.com/json/request_top_list.htm'

    def getPage(self, pageIndex):
        url = self.siteURL + "?page=" + str(pageIndex)
        print(url)
        #request = urllib.Request(url)
        #request = urllib.request.urlopen(url)

        #response = urllib.urlopen(request)
        #return response.read().decode('gbk')
        #return request.decode('gbk')
        http = urllib3.PoolManager()
        r = http.request('GET', url)
        r.status
        return (r.data)

    def getContents(self, pageIndex):
        page = self.getPage(pageIndex)
        pattern = re.compile(
            '<div class="list-item".*?pic-word.*?<a href="(.*?)".*?<img src="(.*?)".*?<a class="lady-name.*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>',
            re.S)
        items = re.findall(pattern, page)
        for item in items:
            print
            item[0], item[1], item[2], item[3], item[4]

if __name__ == '__main__':
    http = urllib3.PoolManager()
    r = http.request('GET', 'http://www.baidu.com/')
    r.status
    print(r.data)

    print(help('urllib3'))
    #spider = Spider()
    #spider.getContents(1)