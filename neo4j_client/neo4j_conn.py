# -*- coding: utf-8 -*-
from py2neo import Graph

class Neo4jConn(object):
    host = '127.0.0.1:7474'
    username = 'neo4j'
    password = 'neo4j'
    graph = Graph('http://%s:%s@%s/db/data' % (username, password, host))

    @classmethod
    def query(cls, statement):
        data = cls.graph.cypher.execute(statement)
        return data

if __name__ == '__main__':
    print(Neo4jConn().graph)