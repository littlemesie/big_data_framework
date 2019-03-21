# encoding: utf-8
import asyncio
from elasticsearch_async import AsyncElasticsearch
from elasticsearch_async.helpers_bulk import bulk
"""
异步es
"""

class AsynEsConn(object):
    """docstring for AsynEsConn"""

    def __init__(self, hosts=None, retry_on_timeout=True, **kwargs):
        self.loop = asyncio.get_event_loop() if kwargs.get("loop", 0) == 0 else kwargs['loop']
        self.es_conn = AsyncElasticsearch(hosts, **kwargs)

    def conn(self):
        return self.es_conn

    async def ping(self, **query_params):
        return await self.es_conn.ping(**query_params)

    async def info(self, **query_params):
        return await self.es_conn.info(**query_params)

    async def create(self, index, doc_type, id, body, **query_params):
        return await self.es_conn.create(index=index, doc_type=doc_type, id=id, body=body, **query_params)

    async def index(self, index, doc_type, body, id=None, **query_params):
        return await self.es_conn.index(index=index, doc_type=doc_type, body=body, id=id, **query_params)

    async def search(self, index=None, doc_type=None, body=None, **query_params):
        return await self.es_conn.search(index=index, doc_type=doc_type, body=body, **query_params)

    async def save_bulk_data(self, actions, stats_only=False, *args, **kwargs):
        return await bulk(self.es_conn, actions=actions, stats_only=stats_only, *args, **kwargs)

    def __del__(self):
        self.loop.run_until_complete(self.es_conn.transport.close())