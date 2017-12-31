SELECT_PROXY_SQL = "select * from proxy where move_status = 0"
SELECT_UA_SQL = "select * from user_agent  where move_status = 0"
SELECT_SOURCE_SQL = "select distinct(name) from source where move_status = 0"
SELECT_CITY_SQL = "select city.key as `key`, city.name as name  from source,city where  city.move_status = 0 and source.name= %s and source.id = city.source_id;"
SELECT_CATEGORY_SQL = "select category.key as `key`, category.name as name  from source,category where  category.move_status = 0 and source.name= %s and source.id = category.source_id"
SELECT_ACCOUNT_SQL="select account.username as username, account.password as password  from source,account where  account.move_status = 0 and source.name= %s and source.id = account.source_id "
SELECT_CONFIG_SQL='select config.login_param as login_param, config.list_page_param as list_page_param,config.content_page_param as content_page_param,config.apply_param as apply_param,config.cancel_param as cancel_param from config,source where  config.move_status = 0 and source.name= %s  and source.id =config.source_id;'