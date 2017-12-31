#! /usr/bin/python
# -*- coding:utf-8 -*-

import pika
from utils import propertiesutil
from utils import logutil

log_util = logutil.LogUtil()

class  RabbitMQUtils(object):

    def __init__(self):
         self.host,\
         self.port,\
         self.virtual_host,\
         self.username,\
         self.password,\
         self.data_exchange,\
         self.fail_exchange = propertiesutil.get_rabbitmq_config()
         credentials = pika.PlainCredentials(self.username,self.password)
         self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host,port=self.port,virtual_host=self.virtual_host ,credentials=credentials))
         self.channel = self.connection.channel()

    def produce_data(self,data):
        self.channel.basic_publish( exchange=self.data_exchange,routing_key='',body=data,  properties=pika.BasicProperties(delivery_mode=2,))




    def produce_fail_data(self,data):
        self.channel.basic_publish( exchange=self.fail_exchange,routing_key='', body=data,properties=pika.BasicProperties(delivery_mode=2,))
