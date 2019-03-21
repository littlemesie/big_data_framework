# -*- coding: utf-8 -*-
from kafka import KafkaConsumer
"""
消费者模块
"""
class Consumer(object):

    def __init__(self, kafka_hosts, kafka_topic):
        self.consumers = KafkaConsumer(kafka_topic,bootstrap_servers=[kafka_hosts])

    def consume(self):
        for message in self.consumers:
            print(message)

if __name__ == '__main__':
    c = Consumer('localhost:9092','my_topic')
    c.consume()