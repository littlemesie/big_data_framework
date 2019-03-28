
import signal
import graphyte
import asyncio
import functools
from mysql_client.mysql_conn import MysqlConn
from mysql_client.pool_wrapper import PoolWrapper

loop = asyncio.get_event_loop()

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
                       port='3306',
                       )

    """docstring for Base_MysqlConn"""

    def __init__(self):
        super(Base_MysqlConn, self).__init__()

# https://graphite.readthedocs.io/en/latest/install.html
# graphyte.init('172.31.38.104', prefix='secheck')
graphyte.init('172.31.9.230', prefix='test')
loop = asyncio.get_event_loop()


async def scan_monitor():
    pending_rate = await _test_rate()
    graphyte.send('secheck.pending_rate', pending_rate)


async def _test_rate():
    async with Base_MysqlConn() as conn:
        cnt = await conn.select_many_one_value(
            """
            select xx from xx order by update_time desc limit 1000
            """
        )
    return cnt.count(20) / 1000



async def run_forever(loop):
    while getattr(loop, 'do_run', True):
        await asyncio.gather(
            scan_monitor(),
        )
        await asyncio.sleep(1)


def shutdown(loop):
    """等待所有任务执行完再退出"""
    print('.........exit.........')
    loop.do_run = False
    pending_tasks = asyncio.Task.all_tasks()
    loop.run_until_complete(asyncio.gather(*pending_tasks))


if __name__ == '__main__':
    print('run...')
    loop.add_signal_handler(signal.SIGTERM, functools.partial(shutdown, loop))
    loop.run_until_complete(run_forever(loop))
