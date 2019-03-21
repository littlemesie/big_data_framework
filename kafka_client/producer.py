# -*- coding: utf-8 -*-
from kafka import KafkaProducer

"""
生产者模块
"""
class Producer(object):

    def __init__(self, kafka_hosts, kafka_topic):
        self.kafka_topic = kafka_topic
        # bootstrap_servers 可以是多台服务器
        self.producer = KafkaProducer(bootstrap_servers=[kafka_hosts])
        self.send()

    def send(self):
        future = self.producer.send('my_topic', key=b'my_key', value=b'my_value', partition=0)
        result = future.get(timeout=10)
        print(result)

if __name__ == '__main__':
    p = Producer('localhost:9092','my_topic')

