# -*- coding:utf-8 -*-

"""
@ide: PyCharm
@author: mesie
@date: 2022/2/28 下午4:13
@summary:
"""
from dbutils.pooled_db import PooledDB
from pymysql.cursors import DictCursor


class PoolWrapper(PooledDB):
    """add cache function"""

    def __init__(self, mincached=0, maxcached=0, maxsize=0, **kwargs):
        kwargs["cursorclass"] = DictCursor
        super(PoolWrapper, self).__init__(**kwargs)
        if maxcached < mincached:
            raise ValueError("maxcached should be not less than mincached")
        # if maxsize < maxcached:
        #     raise ValueError("maxsize should be not less than maxcached")
        # if minsize < mincached:
        #     raise ValueError("minsize should be not less than mincached")
        self._mincached = mincached
        self._maxcached = maxcached
