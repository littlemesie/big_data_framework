import asyncio
from src.mysql_client import MysqlConn
from src.mysql_client import PoolWrapper
loop = asyncio.get_event_loop()
"""使用例子"""
class Base_MysqlConn(MysqlConn):
    pool = PoolWrapper(mincached=1,
                       maxcached=5,
                       minsize=1,
                       maxsize=10,
                       loop=loop,
                       echo=False,
                       pool_recycle=3600,
                       host='127.0.01',
                       user='root',
                       password='123456',
                       db='test',
                       port=3306,
                       )

    """docstring for Base_MysqlConn"""

    def __init__(self):
        super(Base_MysqlConn, self).__init__()

async def test():
    async with Base_MysqlConn() as conn:
        result = await conn.select_one("""select * from xxx where id = xx""")
        await conn.commit()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())