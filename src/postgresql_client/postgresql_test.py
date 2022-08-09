# -*- coding:utf-8 -*-

"""
@ide: PyCharm
@author: mesie
@date: 2022/8/9 14:20
@summary:
"""
import psycopg2
from psycopg2.extras import DictCursor
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
                       database='',
                       port='',
                       cursorclass=DictCursor
                       )

    """docstring for Base_MysqlConn"""

    def __init__(self):
        super(TestConn, self).__init__()