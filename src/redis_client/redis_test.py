# -*- coding: utf-8 -*-
from src.redis_client.redis_conn import RedisConn
redis_host = "127.0.0.1"
redis_port = 6379
redis_db = 0
redis_pwd = "123456"
#项目名称区别key防止冲突
project = "test"
r_conn = RedisConn(host=redis_host, port=redis_port, db=redis_db, password=redis_pwd, project=project)
result = r_conn.set("foo", "bar", ex=60)

result = r_conn.get("foo")
print('result=', result)

result = r_conn.rename("foo", "test")
print('result=', result)

result = r_conn.getset("foo", "bar11")
print(result)