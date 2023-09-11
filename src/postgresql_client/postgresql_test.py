# -*- coding:utf-8 -*-

"""
@ide: PyCharm
@author: mesie
@date: 2022/8/9 14:20
@summary:
"""
import psycopg2
from psycopg2.extras import RealDictCursor
from postgresql_client.postgresql_conn import PostgresqlConn
from postgresql_client.pool_wrapper import PoolWrapper

class TestConn(PostgresqlConn):
    pool = PoolWrapper(creator=psycopg2,
                       maxcached=5,
                       mincached=1,
                       maxconnections=10,
                       host='127.0.0.1',
                       user='postgres',
                       password='postgres',
                       database='aia',
                       port='5432',
                       cursor_factory=RealDictCursor
                       )

    """docstring for Base_MysqlConn"""

    def __init__(self):
        super(TestConn, self).__init__()



def t():
    with TestConn() as conn:
        data = conn.select_one(
            """
            select * from aia_t_icc_jjdb limit 1
            """
        )
    print(data)

# t()
