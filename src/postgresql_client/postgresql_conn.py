# -*- coding:utf-8 -*-

"""
@ide: PyCharm
@author: mesie
@date: 2022/8/9 13:56
@summary:
"""
class PostgresqlConn(object):
    pool = None
    def __init__(self):
        self._conn = None
        self._cur = None

    def select_one(self, sql, params=None):
        try:
            self._cur.execute(sql, params)
            result = self._cur.fetchone()
            if result:
                return dict(result)
            else:
                return None
        except Exception as e:
            self.rollback()
            raise e

    def select_one_value(self, sql, params=None):
        try:
            self._cur.execute(sql, params)
            result = self._cur.fetchone()
            if result:
                return list(dict(result).values())[0]
            else:
                return None
        except Exception as e:
            self.rollback()
            raise e

    def select_many(self, sql, params=None):
        try:
            self._cur.execute(sql, params)
            result = self._cur.fetchall()
            if result:
                return list(map(lambda one: dict(one), result))
            else:
                return []
        except Exception as e:
            self.rollback()
            raise e

    def select_many_one_value(self, sql, params=None):
        try:
            self._cur.execute(sql, params)
            result = self._cur.fetchall()
            if result:
                return list(map(lambda one: list(dict(one).values())[0], result))
            else:
                return []
        except Exception as e:
            self.rollback()
            raise e

    def insert_one(self, sql, params=None, return_auto_increament_id=False):
        try:
            self._cur.execute(sql, params)
            if return_auto_increament_id:
                return self._cur.lastrowid
        except Exception as e:
            self.rollback()
            raise e

    def insert_many(self, sql, params):
        try:
            count = self._cur.executemany(sql, params)
            return count
        except Exception as e:
            self.rollback()
            raise e

    def update(self, sql, params=None):
        try:
            result = self._cur.execute(sql, params)
            return result
        except Exception as e:
            self.rollback()
            raise e

    def delete(self, sql, params=None):
        try:
            result = self._cur.execute(sql, params)
            return result
        except Exception as e:
            self.rollback()
            raise e

    def begin(self):
        self._conn.begin()

    def commit(self):
        try:
            self._conn.commit()
        except Exception as e:
            self.rollback()
            raise e

    def rollback(self):
        self._conn.rollback()

    def close(self):
        self.pool.close()
        self.pool.wait_closed()

    def executed(self):
        return self._cur._executed

    def __enter__(self):
        self._conn = self.pool.connection()
        self._cur = self._conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self._cur.close()