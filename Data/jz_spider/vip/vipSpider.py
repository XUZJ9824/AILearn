#! /usr/bin/python
# -*- coding: utf-8 -*-

import pycurl
import StringIO
import json
import urllib
import random
import redis
import MySQLdb
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
TIMEOUT = 5
CONNECT_TIMEOUT = 5


ENCODING = 'gzip'
POST = 'post'
GET = 'get'
USER_AGENT=["Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
            "Mozilla/4.0 (compatible; MSIE 5.0; Windows NT)",
             "Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1",
             "Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3",
             "Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12",
             "Opera/9.27 (Windows NT 5.2; U; zh-cn)",
             "Opera/8.0 (Macintosh; PPC Mac OS X; U; en)",
             "Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0 ",
             "Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Version/3.1",
             "Mozilla/5.0 (iPhone; U; CPU like Mac OS X) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/4A93",
             "Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27",
             "Mozilla/5.0 (Linux; U; Android 4.0.3; zh-cn; M032 Build/IML74K) AppleWebKit/533.1 (KHTML, like Gecko)Version/4.0 MQQBrowser/4.1 Mobile Safari/533.1",
             "MQQBrowser/38 (iOS 4; U; CPU like Mac OS X; zh-cn)"
            ]

def download(req_json):
    request = pycurl.Curl();
    request.setopt(pycurl.URL, req_json['url'])
    if req_json['method']==GET:
        request.setopt(pycurl.POST, 0)
    elif req_json['method'] == POST:
         request.setopt(pycurl.POST, 1)
         post_param = urllib.urlencode(json.loads(req_json['post_data']))
         request.setopt(pycurl.POSTFIELDS, post_param)
    request.setopt(pycurl.CONNECTTIMEOUT, TIMEOUT)
    request.setopt(pycurl.TIMEOUT, CONNECT_TIMEOUT)
    request.setopt(pycurl.ENCODING,ENCODING)
    if 'cookie' in req_json.keys():
        if req_json['cookie']:
          request.setopt(pycurl.COOKIE,req_json['cookie'])
    ua = random.choice(USER_AGENT)
    request.setopt(pycurl.USERNAME, ua)
    if 'ip' in req_json.keys() and  'port' in req_json.keys():
        request.setopt(pycurl.PROXY, 'http://%s:%s' % (req_json['ip'],req_json['port']))
    body = StringIO.StringIO()
    request.setopt(pycurl.WRITEFUNCTION, body.write)
    request.perform()
    response = body.getvalue()
    return response,request


def parse_58_vip():
    page_url_format = 'https://qjzapi.58.com/api/?appKey=1&isNeedBalance=1&method=renwu.list&isNeedTaskMyCnt=1&v=1.0&page=%s'
    detail_url_format = 'https://qjzapi.58.com/api/?method=renwu.detail&v=1.0&appKey=1&taskId=%s'
    page_num = 1
    while True:
        page_url = page_url_format % page_num
        req_json = {"url":page_url,"method":"get"}
        #print page_url
        body,request = download(req_json)
        js = json.loads(body)
        json_data_list = js['result']['data']['tasks']
        if len(json_data_list) > 0:
            for json_data in json_data_list:
                try:
                    sql_map = {}
                    id = json_data['taskId']
                    flag = existsKey("58_vip_"+id)
                    if flag is False:
                        req_json = {"url":detail_url_format % id,"method":"get"}
                        body,request = download(req_json)
                        js =json.loads(body)
                        sql_map['job_id'] = id;
                        sql_map['job_site'] = "58_vip";
                        sql_map['salary'] = js['result']['data']['taskBaseInfo']['price']+js['result']['data']['taskBaseInfo']['unit']
                        sql_map['title'] = js['result']['data']['taskBaseInfo']['title']
                        steps = js['result']['data']['taskSteps']['steps']
                        job_desc = ''
                        for step in steps:
                            job_desc = job_desc+step['desc']
                        sql_map['job_desc'] = job_desc
                        sql = generate_sql(sql_map)
                        insert(sql)
                        #setKey("58_vip_"+id)
                except Exception as ex:
                    #print ex
                    continue
        else:break
        page_num +=1



import re
def parse_koudai_vip():
    page_url_format = 'http://m.kdjz.com/micro-tasks/list/index?provinceId=3JnyBQ87g1REZrVXjR5a&sort=new&page=%s'
    detail_url_format = 'http://m.kdjz.com/micro-tasks?microTaskId=%s'
    page_num = 1
    while True:

        page_url = page_url_format % page_num
        req_json = {"url":page_url,"method":"get"}
        print(page_url)

        body,request = download(req_json)
        if page_num ==1:
            json_data_list =  re.findall('<a href="([\s\S]*?)"',body)
        else:
            js = json.loads(body)
            json_data_list = js['data']['microTasks']
        if len(json_data_list) > 0:
            for json_data in json_data_list:
                try:
                    sql_map = {}
                    if page_num ==1:
                        detailLink = json_data
                    else:
                        detailLink = json_data['detailLink']
                    id = str(detailLink.replace("http://m.kdjz.com/micro-tasks?microTaskId=",""))
                    flag = existsKey("koudai_vip_"+id)
                    if flag is False:
                        req_json = {"url":detail_url_format % id,"method":"get"}
                        body,request = download(req_json)
                        sql_map['job_id'] = id;
                        sql_map['job_site'] = "koudai_vip";
                        sql_map['salary'] =get_value('<span class="biger">([\s\S]*?)</span>',body)
                        sql_map['title'] = get_value('<div class="mask">([\s\S]*?)</div>',body)
                        sql_map['job_desc'] = get_value('<div class="content">([\s\S]*?)<div class="detail-blick" id="fourth">',body)
                        #print sql_map
                        sql = generate_sql(sql_map)
                        print(sql)
                        insert(sql)
                        #setKey("koudai_vip_"+id)
                except Exception as ex:
                    #print ex
                    continue
        else:break
        page_num +=1



def parse_jianzhiku_vip():
    page_url_format = 'http://www.jianzhiku.com/earn/thirdpartytask'
    post_data_format = '{"action":"GetList","version":48,"pindex":%s,"type":7,"subtype":1}'
    thirdpartytask_url = 'http://www.jianzhiku.com/earn/thirdpartytask'
    thirdpartytask_post_data = '{"action":"GetDetail","version":48,"earnid":%s}'
    missionAction_url= 'http://www.jianzhiku.com/earn/MissionAction'
    missionAction_post_data = '{"action":"MissionDetail","version":48,"earnid":%s}'
    page_num = 1
    while True:
        post_data = post_data_format % page_num
        req_json = {"url":page_url_format,"method":"post","post_data":post_data}
        body,request = download(req_json)
        js = json.loads(body)
        json_data_list = js
        if len(json_data_list) > 0:
            for json_data in json_data_list:
                try:
                    sql_map = {}
                    id = json_data['id']
                    flag = existsKey("58_jianzhiku_"+str(id))
                    if flag is False:
                        req_json = {"url":thirdpartytask_url ,"method":"post","post_data":thirdpartytask_post_data % id,"cookie":'.ASPXAUTH=463A1531E7D7A29E53774D0E3522107645F25FCC9083723089DAE2823E05988BE8551276A258B85C7DDC58EB6EC2F4BB6F513E7088145C203799D698D5384649BD128369D5A46789F96F85DE44AAA1931BDF09CC03238F31381C5E0D6856FD887CA2398EB12024E3D41D015FA853036429F0AB7C43BB8E304082BD06FC6B4CB393822E2A2913D3C92CC17A67F3E8AE5F; WapTaskCookie=fromtype=ioszrb'}
                        body,request = download(req_json)
                        req_json = {"url":missionAction_url ,"method":"post","post_data":missionAction_post_data % id,"cookie":'.ASPXAUTH=463A1531E7D7A29E53774D0E3522107645F25FCC9083723089DAE2823E05988BE8551276A258B85C7DDC58EB6EC2F4BB6F513E7088145C203799D698D5384649BD128369D5A46789F96F85DE44AAA1931BDF09CC03238F31381C5E0D6856FD887CA2398EB12024E3D41D015FA853036429F0AB7C43BB8E304082BD06FC6B4CB393822E2A2913D3C92CC17A67F3E8AE5F; WapTaskCookie=fromtype=ioszrb'}
                        action_body,request = download(req_json)
                        js =json.loads(body)
                        action_js = json.loads(action_body)
                        sql_map['job_id'] = id;
                        sql_map['job_site'] = "58_jianzhiku";
                        sql_map['salary'] = js['money']
                        sql_map['title'] = js['name']
                        steps = action_js
                        job_desc = ''
                        for step in steps:
                            job_desc = job_desc+step['detail']
                        sql_map['job_desc'] = job_desc
                        sql = generate_sql(sql_map)
                        print(sql)
                        insert(sql)
                        setKey("58_jianzhiku_"+str(id))

                except Exception as ex:
                    print(ex)
                    continue
        else:break
        page_num +=1


redis_host = '10.1.188.206'
redis_port = 6380
def existsKey(key):
    client=redis.Redis(host=redis_host,port=redis_port)
    return client.exists(key)

def setKey(key):
    client=redis.Redis(host=redis_host,port=redis_port)
    client.set(key,int(time.time()))
    client.expire(key,7776000)

REMOVE_REG_REGEX = '<[^>]*>'
REMOVE_BLANK_REGEX = '[\\s]{2,}'
def get_value(parse_key,body):
    value = re.findall(parse_key,body)
    if len(value) != 0:
        value = re.sub(REMOVE_REG_REGEX,'',value[0])
        value =re.sub(REMOVE_BLANK_REGEX,'',value)
        value =re.sub('&nbsp;',' ',value)
        return value



DB_HOST ='10.216.103.43'
BD_USER = 'root'
BD_PASSWD = 'root'
DB_NAME = 'spider_online'
DB_PORT = 3306
DB_CHARSET = 'utf8'

# DB_HOST ='g1-grab-ku-w.dns.doumi.com'
# BD_USER = 'grab_data_w'
# BD_PASSWD = 'M9J8h%e4UkI0o3Iq1%'
# DB_NAME = 'grab_data'
# DB_PORT  = 3937
# DB_CHARSET = 'utf8'


def select_all_value(sql):
    conn = MySQLdb.connect(host=DB_HOST, user=BD_USER, passwd=BD_PASSWD, db=DB_NAME, port=int(DB_PORT), charset=DB_CHARSET)
    cursor = conn.cursor()
    cursor.execute (sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def insert(sql):
    conn = MySQLdb.connect(host=DB_HOST, user=BD_USER, passwd=BD_PASSWD, db=DB_NAME, port=int(DB_PORT), charset=DB_CHARSET)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

def write_file(msg):
    timestamp = time.strftime('%Y-%m-%d')
    file_name = timestamp + '.log'
    file_obj=open(file_name,'a')
    file_obj.write(msg+'\n')
    file_obj.close()

def generate_sql(sql_map):
    sql_field = sql_map.keys()
    sqlStr = 'INSERT INTO %s SET ' % ('jianzhi')
    sqlStr += ','.join('='.join(['`%s`'%i,'\'%s\''% sql_map[i]]) for i in sql_field)
    sqlStr += ';'
    return sqlStr


if __name__ == '__main__':
    parse_58_vip()