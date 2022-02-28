# -*- coding:utf-8 -*-

"""
@ide: PyCharm
@author: mesie
@date: 2022/2/28 下午4:22
@summary:
"""
import pymysql
from mysql_client.mysql_conn import MysqlConn
from mysql_client.pool_wrapper import PoolWrapper
"""使用例子"""

def test():
    pool = PoolWrapper(creator=pymysql,
                       maxcached=5,
                       mincached=1,
                       maxconnections=10,
                       host='127.0.0.1',
                       user='root',
                       password='123456',
                       db='xxx',
                       port=3306,
                       )
    conn = pool.connection()
    cur = conn.cursor()
    con = MysqlConn(conn, cur)
    result = con.select_one("""select * from xx where id = xx""")
    print(result)

if __name__ == '__main__':
    test()