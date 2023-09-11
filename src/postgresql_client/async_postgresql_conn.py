# -*- coding: utf-8 -*-
"""
@date: 2023/9/11 下午2:09
@summary:
"""
import logging
import asyncio
import traceback
from asyncpg import create_pool


class PostgresqlConn(object):

    def __init__(self, max_size=5, min_size=1, host='127.0.0.1', user='postgres', password='postgres',
                 database='test', port='5432', loop=asyncio.get_event_loop()):
        self.max_size = max_size
        self.min_size = min_size
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.loop = loop
        self._conn = None
        self._cur = None

    async def _create_pool(self):
        pool = await create_pool(
            max_size=self.max_size,
            min_size=self.min_size,
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port,
            loop=self.loop
        )
        return pool


    async def select_one(self, sql, *params):
        try:
            result = await self._conn.fetch(sql, *params)
            if len(result) > 0:
                return dict(result[0])
            else:
                return None
        except Exception as e:
            logging.error(traceback.format_exc())
            await self.release()
            raise e

    async def select_one_value(self, sql, *params):
        try:
            result = await self._conn.fetch(sql, *params)
            print(result)
            if len(result) > 0:
                return list(dict(result[0]).values())[0]
            else:
                return None
        except Exception as e:
            logging.error(traceback.format_exc())
            await self.release()
            raise e

    async def select_many(self, sql, *params):
        try:
            result = await self._conn.fetch(sql, *params)
            if len(result) > 0:
                return [dict(one) for one in result]
            else:
                return []
        except Exception as e:
            logging.error(traceback.format_exc())
            await self.release()
            raise e

    async def select_many_one_value(self, sql, *params):
        try:
            result = await self._conn.fetch(sql, *params)
            if len(result) > 0:
                return [list(dict(one).values())[0] for one in result]
            else:
                return []
        except Exception as e:
            logging.error(traceback.format_exc())
            await self.release()
            raise e

    async def insert_one(self, sql, *params, return_auto_increament_id=False):
        try:
            await self._conn.fetch(sql, *params)
            if return_auto_increament_id:
                return self._conn.lastrowid
        except Exception as e:
            logging.error(traceback.format_exc())
            await self.release()
            raise e

    async def insert_many(self, sql, *params):
        try:
            count = await self._conn.fetch(sql, *params)
            return count
        except Exception as e:
            logging.error(traceback.format_exc())
            await self.release()
            raise e

    async def update(self, sql, *params):
        try:
            result = await self._conn.fetch(sql, params)
            return result
        except Exception as e:
            logging.error(traceback.format_exc())
            await self.release()
            raise e

    async def delete(self, sql, *params):
        try:
            result = await self._conn.fetch(sql, *params)
            return result
        except Exception as e:
            logging.error(traceback.format_exc())
            await self.release()
            raise e

    async def begin(self):
        await self._conn.begin()

    async def commit(self):
        try:
            await self._conn.commit()
        except Exception as e:
            logging.error(traceback.format_exc())
            await self.release()
            raise e


    async def close(self):
        await self.pool.close()

    def executed(self):
        return self._conn._executed

    async def release(self):
        await self.pool.release(self._conn)

    async def __aenter__(self):
        self.pool = await self._create_pool()
        self._conn = await self.pool.acquire()
        return self

    async def __aexit__(self,  *exc):
        await self._conn.close()
