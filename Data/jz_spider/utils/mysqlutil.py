#! /usr/bin/python
# -*- coding: utf-8 -*-

from utils import propertiesutil
#import MySQLdb #python2
import pymysql as MySQLdb


class MySqlUtil(object):
    def __init__(self):
        host, \
        username, \
        password, \
        port, \
        db_name, \
        charset = propertiesutil.get_mysql_config()
        self.conn = MySQLdb.connect(host=host,
                                    user=username,
                                    passwd=password,
                                    db=db_name,
                                    port=int(port),
                                    charset=charset)

    def select(self, sql):
        try:
            self.cursor = self.conn.cursor(cursor=MySQLdb.cursors.DictCursor)
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except Exception as ex:
            print("error msg %s" % ex.message)
        finally:
            self.cursor.close()

    def insert(self, sql):
        try:
            self.cursor = self.conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as ex:
            print("error msg %s" % ex.message)
        finally:
            self.cursor.close()

    def update(self, sql):
        try:
            self.cursor = self.conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as ex:
            print("error msg %s" % ex.message)
        finally:
            self.cursor.close()


if __name__ == '__main__':
    mysql_util = MySqlUtil()
    mysql_util.select("SELECT * FROM jianzhi LIMIT 1")
