
import json
import logging
import threading

from kazoo.client import KazooClient, KeeperState
from thrift import Thrift
from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket
from thrift.transport import TTransport

from src.kazoo_client.thrift_sussion.sussion import TSussionService

logger = logging.getLogger()


class SussionClient(object):

    thrift_clients = []
    client_index = 0
    retry_time = 3
    _instance_lock = threading.Lock()
    Authzk_Hosts = None
    zk = KazooClient(hosts="127.0.0.1:3181")

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = object.__new__(cls)
        return cls._instance

    @classmethod
    def get_clients_list(cls):
        return cls.thrift_clients

    @classmethod
    def get_one_client(cls):
        cls.client_index += 1
        clients_length = len(cls.thrift_clients)
        if clients_length == 0:
            return None
        else:
            return cls.thrift_clients[cls.client_index % clients_length]

    @classmethod
    def init_clients(cls, Authzk_Hosts):
        cls.Authzk_Hosts = Authzk_Hosts
        cls.zk = KazooClient(hosts=Authzk_Hosts)
        with cls._instance_lock:
            cls.thrift_clients = []
            if (cls.zk.client_state != KeeperState.CONNECTED and cls.zk.client_state != KeeperState.CONNECTED_RO):
                cls.zk.restart()
            children = cls.zk.get_children("/com/xxx/sussion", watch=cls.children_callback)
            for child in children:
                info = cls.zk.get("/com/xxx/sussion/" + child)
                node = json.loads(info[0])
                try:
                    transport = TSocket.TSocket(host=node['host'], port=node['thriftPort'])
                    transport = TTransport.TFramedTransport(transport)
                    protocol = TBinaryProtocol.TBinaryProtocol(transport)
                    thrift_client = TSussionService.Client(protocol)
                    transport.open()
                    cls.thrift_clients.append(thrift_client)
                    logger.info("thrift client open!")
                except Thrift.TException as ex:
                    logger.error("thrift connect error:%s" % (ex.message))

    @classmethod
    def children_callback(cls, event):
        logger.info("SussionClient children_callback event {}".format(event))
        cls.init_clients(cls.Authzk_Hosts)

    @classmethod
    def reset_retry_time(cls):
        cls.retry_time = 3
