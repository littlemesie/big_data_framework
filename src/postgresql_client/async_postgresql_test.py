# -*- coding:utf-8 -*-

"""
@date: 2023/9/11 下午2:09
@summary:
"""
import asyncio
from asyncpg import create_pool
from postgresql_client.async_postgresql_conn import PostgresqlConn

loop = asyncio.get_event_loop()

class AsyncTestConn(PostgresqlConn):

    """docstring for AsyncTestConn"""

    def __init__(self):
        super(AsyncTestConn, self).__init__(max_size=5,
                       min_size=1,
                       host='127.0.0.1',
                       user='postgres',
                       password='postgres',
                       database='aia',
                       port='5432',
                       loop=loop)


async def async_t():
    async with AsyncTestConn() as conn:
        data = await conn.select_many_one_value(
            """
            select jjdbh from aia_t_icc_jjdb limit 10
            """,
        )
    print(data)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_t())

