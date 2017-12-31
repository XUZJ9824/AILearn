#! /usr/bin/python
# -*- coding: utf-8 -*-


#import configparser #python 2
import configparser #python 3
from constant import charset as chrset
import os

def get_mysql_config():
    config_path ='\\'.join([os.getcwd(),"\conf\config.properties"])
    config = configparser.ConfigParser()
    config.read(filenames=config_path, encoding=chrset.UTF8)
    host = config.get('mysql','host')
    username = config.get('mysql','username')
    password = config.get('mysql','password')
    port = int(config.get('mysql','port'))
    db_name = config.get('mysql','db_name')
    charset = config.get('mysql','charset')
    return host,username,password,port,db_name,charset

def get_rabbitmq_config():
    config_path ='\\'.join([os.getcwd(),"\conf\config.properties"])
    config = configparser.ConfigParser()
    config.read(config_path)
    host = config.get('rabbitmq','host')
    port = int(config.get('rabbitmq','port'))
    virtual_host = config.get('rabbitmq','virtual_host')
    username = config.get('rabbitmq','username')
    password = config.get('rabbitmq','password')
    data_exchange = config.get('rabbitmq','data_exchange')
    fail_exchange = config.get('rabbitmq','fail_exchange')

    return host,port,virtual_host,username,password,data_exchange,fail_exchange

def get_redis_config():
    config_path ='\\'.join([os.getcwd(),"\conf\config.properties"])
    config = configparser.configparser()
    config.read(config_path)
    host = config.get('redis','host')
    port = int(config.get('redis','port'))
    return host,port

def get_statsd_config():
    config_path ='\\'.join([os.getcwd(),"\conf\config.properties"])
    config = configparser.configparser()
    config.read(config_path)
    host = config.get('statsd','host')
    port = int(config.get('statsd','port'))
    prefix = config.get('statsd','prefix')
    return host,port,prefix



