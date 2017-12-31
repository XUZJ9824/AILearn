#! /usr/bin/python
# -*- coding: utf-8 -*-
import logging
import logging.config
import os

class LogUtil(object):

    def __init__(self):
        log_path ='\\'.join([os.getcwd(),"\conf\logging.conf"])
        print(log_path)
        logging.config.fileConfig(log_path)
        self.log_error = logging.getLogger('errorLogger')
        self.log_info = logging.getLogger('infoLogger')

    def info(self,msg):
        self.log_info.info(msg)

    def error(self,msg):
        self.log_info.info(msg)

if __name__ == '__main__':
    log = LogUtil()

