#! /usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb
import json
import time
host='10.216.103.18'
username='root'
password = 'root'
db_name = 'spider_online'
port = 3306
charset = 'utf8'

class MysqlUtilTest(object):
    def __init__(self):
        self.conn = MySQLdb.connect(host=host,
                               user=username,
                               passwd=password,
                               db=db_name,
                               port=int(port),
                               charset=charset)
    def select(self,sql):
        cursor = self.conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        sql = "select all_city,all_type from assembly_url_rule where job_site ='58'"
        cursor.execute(sql)
        result = cursor.fetchone()
        return result

    def insert(self,sql):
        cursor = self.conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        sql = "select all_city,all_type from assembly_url_rule where job_site ='58'"
        cursor.execute(sql)

if __name__ == '__main__':
    result  = select("")

    all_city = result['all_city']
    all_city =  json.loads(all_city)
    for city in all_city:
         "INSERT INTO city set key = '%s',name='%s',source_id=%s,create_at =%s;" % ( city,all_city[city],1,int(time.time()))