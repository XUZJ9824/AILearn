__author__ = 'CQC'
# -*- coding:utf-8 -*-

#encoding:UTF-8
import urllib.request
import re
import urllib
from collections import deque
import sys
from itertools import groupby


def test1():
    queue = deque()
    visited = set()

    url = "http://www.baidu.com"
    queue.append(url)
    url = 'https://www.baidu.com/s?word=Jecvay+Notes'
    queue.append(url)

    cnt = 0

    while queue and (cnt < 200):
        url=queue.popleft()
        visited|={url}
        print("Grab %s, %s" % (str(cnt),url))

        cnt +=1
        try:
            data = urllib.request.urlopen(url).read()
            data = data.decode('UTF-8')
        except Exception as err:
            print('Error : ' + str(err))
            continue

        #print(data)

        linkre = re.compile('href=\"(.+?)\"')
        for x in linkre.findall(data):
            if 'http' in x and x not in visited:
                queue.append(x)
                print('Add Queue --->  ' + x)

    return

def test2():
    data = {}
    data['word'] = 'Jecvay Notes'

    url_values = urllib.parse.urlencode(data)
    url = "http://www.baidu.com/s?"
    full_url = url + url_values

    data = urllib.request.urlopen(full_url).read()
    data = data.decode('UTF-8')
    print(data)
    return

def test3():
    data = {}

    queue = deque()
    visited = set()

    url = 'https://www.baidu.com/s?word=Jecvay+Notes'  # 入口页面, 可以换成别的
    queue.append(url)

    url = 'https://www.baidu.com'
    queue.append(url)

    cnt = 0

    while queue:
        url = queue.popleft()  # 队首元素出队
        visited |= {url}  # 标记为已访问

        print('已经抓取: ' + str(cnt) + '   正在抓取 <---  ' + url)
        cnt += 1
        #urlop = urllib.request.urlopen(url)
        #if 'html' not in urlop.getheader('Content-Type'):
        #    continue

        # 避免程序异常中止, 用try..catch处理异常
        #try:
        #data = urlop.read().decode('utf-8')

        data = urllib.request.urlopen(url).read()
        data = data.decode('UTF-8')

        print(data)
        #except:
        #    continue

        # 正则表达式提取页面中所有队列, 并判断是否已经访问过, 然后加入待爬队列
        linkre = re.compile('href=\"(.+?)\"')
        for x in linkre.findall(data):
            if 'http' in x and x not in visited:
                queue.append(x)
                print('加入队列 --->  ' + x)

def split(l):
  r = []
  last = -1
  for i in l:
    if last == i:
      r[-1].append(i)
    else:
      r.append([i])
      last = i

  #another way to make the same result
  r2 = list(map(lambda x: list(x[1]), groupby([0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0])))
  return r

if __name__ == '__main__':
    #test1()
    #test2()
    #test3()
    l1 = [0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0]
    l2 = split(l1);