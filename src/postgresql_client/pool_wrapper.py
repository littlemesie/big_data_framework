# -*- coding:utf-8 -*-

"""
@ide: PyCharm
@author: mesie
@date: 2022/8/9 14:02
@summary:
"""

from psycopg2.extras import DictCursor
from dbutils.pooled_db import PooledDB


class PoolWrapper(PooledDB):
    """add cache function"""

    def __init__(self, mincached=0, maxcached=0, maxsize=0, **kwargs):
        kwargs["cursor_factory"] = DictCursor
        super(PoolWrapper, self).__init__(**kwargs)
        if maxcached < mincached:
            raise ValueError("maxcached should be not less than mincached")
        self._mincached = mincached
        self._maxcached = maxcached

    def release(self, conn):
        pass