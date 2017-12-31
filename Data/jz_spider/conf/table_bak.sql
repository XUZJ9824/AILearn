use spider_data;
CREATE TABLE IF NOT EXISTS `spider_data`.`source` (
 `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
 `name` varchar(255) NOT NULL DEFAULT '' COMMENT '数据源名称',
 `domain` varchar(255) NOT NULL DEFAULT '' COMMENT '数据源域名',
 `create_at` int(11) NOT NULL DEFAULT '0' COMMENT '创建时间',
 `modify_at` int(11) NOT NULL DEFAULT '0' COMMENT '最后修改时间',
 `move_status` int(11) NOT NULL DEFAULT '0' COMMENT '0 1',
 PRIMARY KEY (`id`) ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='数据源表';

use spider_data;
CREATE TABLE IF NOT EXISTS `spider_data`.`city` (
 `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
 `key` varchar(255) NOT NULL DEFAULT '' COMMENT '城市key值',
 `name` varchar(255) NOT NULL DEFAULT '' COMMENT '城市名称',
 `source_id` int(11) NOT NULL DEFAULT '0' COMMENT '数据源id',
 `create_at` int(11) NOT NULL DEFAULT '0' COMMENT '创建时间',
 `modify_at` int(11) NOT NULL DEFAULT '0' COMMENT '最后修改时间',
 `move_status` int(11) NOT NULL DEFAULT '0' COMMENT '0 1',
 PRIMARY KEY (`id`) ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='城市表';


use spider_data;
CREATE TABLE IF NOT EXISTS `spider_data`.`category` (
 `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
 `key` varchar(255) NOT NULL DEFAULT '' COMMENT '类目key值',
 `name` varchar(255) NOT NULL DEFAULT '' COMMENT '类目名称',
 `source_id` int(11) NOT NULL DEFAULT '0' COMMENT '数据源id',
 `create_at` int(11) NOT NULL DEFAULT '0' COMMENT '创建时间',
 `modify_at` int(11) NOT NULL DEFAULT '0' COMMENT '最后修改时间',
 `move_status` int(11) NOT NULL DEFAULT '0' COMMENT '0 1',
 PRIMARY KEY (`id`) ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='类目表';



use spider_data;
CREATE TABLE IF NOT EXISTS `spider_data`.`config` (
 `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
 `login_param` text NOT NULL DEFAULT '' COMMENT '登陆参数',
 `list_page_param` text NOT NULL DEFAULT '' COMMENT '列表页参数',
 `content_page_param` text NOT NULL DEFAULT '' COMMENT '内容页参数',
 `apply_param` text NOT NULL DEFAULT '' COMMENT '申请报名参数',
 `cancel_param` text NOT NULL DEFAULT '' COMMENT '取消报名参数',
 `source_id` int(11) NOT NULL DEFAULT '0' COMMENT '数据源id',
 `create_at` int(11) NOT NULL DEFAULT '0' COMMENT '创建时间',
 `modify_at` int(11) NOT NULL DEFAULT '0' COMMENT '最后修改时间',
 `move_status` int(11) NOT NULL DEFAULT '0' COMMENT '0 1',
 PRIMARY KEY (`id`) ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='配置表';

use spider_data;
CREATE TABLE IF NOT EXISTS `spider_data`.`jz_data` (
 `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
 `source_id` int(11) NOT NULL DEFAULT '0' COMMENT '数据源id',
 `city_id` int(11) NOT NULL DEFAULT '0' COMMENT '城市id',
 `category_id` int(11) NOT NULL DEFAULT '0' COMMENT '类目id',
 `fields` text NOT NULL DEFAULT '' COMMENT '字段数据',
 `create_at` int(11) NOT NULL DEFAULT '0' COMMENT '创建时间',
 `modify_at` int(11) NOT NULL DEFAULT '0' COMMENT '最后修改时间',
 `move_status` int(11) NOT NULL DEFAULT '0' COMMENT '0 1',
 PRIMARY KEY (`id`) ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='配置表';

use spider_data;
CREATE TABLE IF NOT EXISTS `spider_data`.`user_agent` (
 `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
 `platform_type` varchar(255) NOT NULL DEFAULT '' COMMENT '平台类型',
 `value` text NOT NULL DEFAULT '' COMMENT 'ua值',
 `create_at` int(11) NOT NULL DEFAULT '0' COMMENT '创建时间',
 `modify_at` int(11) NOT NULL DEFAULT '0' COMMENT '最后修改时间',
 `move_status` int(11) NOT NULL DEFAULT '0' COMMENT '0 1',
 PRIMARY KEY (`id`) ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='ua表';


use spider_data;
CREATE TABLE IF NOT EXISTS `spider_data`.`proxy` (
 `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
 `protocol` varchar(255) NOT NULL DEFAULT '' COMMENT '协议',
 `ip` varchar(255) NOT NULL DEFAULT '' COMMENT 'ip',
 `port` int(11) NOT NULL DEFAULT '0' COMMENT '端口号',
 `username` varchar(255) NOT NULL DEFAULT '' COMMENT '用户名',
 `password` varchar(255) NOT NULL DEFAULT '' COMMENT '密码',
 `create_at` int(11) NOT NULL DEFAULT '0' COMMENT '创建时间',
 `modify_at` int(11) NOT NULL DEFAULT '0' COMMENT '最后修改时间',
 `move_status` int(11) NOT NULL DEFAULT '0' COMMENT '0 1',
 PRIMARY KEY (`id`) ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='代理ip表';


use spider_data;
CREATE TABLE IF NOT EXISTS `spider_data`.`account` (
 `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
 `username` varchar(255) NOT NULL DEFAULT '' COMMENT '用户名',
 `password` varchar(255) NOT NULL DEFAULT '' COMMENT '密码',
 `source_id` int(11) NOT NULL DEFAULT '0' COMMENT '数据源id',
 `create_at` int(11) NOT NULL DEFAULT '0' COMMENT '创建时间',
 `modify_at` int(11) NOT NULL DEFAULT '0' COMMENT '最后修改时间',
 `move_status` int(11) NOT NULL DEFAULT '0' COMMENT '0 1',
 PRIMARY KEY (`id`) ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='账号表';




