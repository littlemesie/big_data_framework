# -*- coding: utf-8 -*-

import happybase
import logging



class HappyBaseClient(object):
    def __init__(self):
        self.connection = happybase.Connection('172.31.17.254')

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            logging.error(exc_type)
            logging.error(exc_val)
            logging.error(exc_tb)
        self.close()

if __name__ == '__main__':
    pass

