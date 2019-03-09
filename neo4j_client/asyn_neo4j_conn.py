# -*- coding: utf-8 -*-
from aioneo4j import Neo4j
from neo4j_client import hydrate


class AsynNeo4jConn(object):
    """docstring for AsynNeo4jConn"""

    def __init__(self, username, password, host='127.0.0.1:7474', request_timeout=10, loop=None):
        self.__url = f'http://{username}:{password}@{host}/'
        self.__conn = Neo4j(self.__url)

    async def query(self, sql):
        data = await self.__conn.cypher(sql)
        return hydrate.hydrate(data)

    async def close(self):
        await self.__conn.close()