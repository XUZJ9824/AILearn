#! /usr/bin/python
# -*- coding: utf-8 -*-

import time

fields =['job_type', 'height', 'ability_req', 'created_time', 'interview_addr', 'apply_end_time', 'settlement', 'job_site', 'city', 'job_id', 'title', 'work_area', 'work_addr', 'id', 'need_count', 'company_name', 'percentage', 'start_date', 'work_date', 'qq', 'end_date', 'max_age', 'weixin', 'start_time', 'work_time', 'min_age', 'phone', 'special_req', 'interview_time', 'sex', 'identity', 'job_desc', 'salary', 'salary_remarks', 'age', 'contacts', 'email', 'move_status', 'publish_date', 'end_time', 'salary_unit']

def handle(source,city,category,url,field_map):
    field_map['job_site'] =source
    field_map['city'] =city['name']
    field_map['job_type'] =category['name']
    field_map['job_id'] =url
    field_map['created_time'] = int(time.time())
    for field in fields:
        if field not in field_map.keys():
            field_map[field] = ''
    return field_map