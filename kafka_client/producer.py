# -*- coding: utf-8 -*-
from kafka import KafkaProducer

"""
生产者模块
"""
class Producer(object):

    def __init__(self, kafka_host, kafka_port, kafka_topic):
        self.kafka_topic = kafka_topic
        # bootstrap_servers 可以是多台服务器
        self.producer = KafkaProducer(bootstrap_servers=['{kafka_host}:{kafka_port}'.format(kafka_host=kafka_host,kafka_port=kafka_port)])
        self.produce()

    def produce(self):
        for i in range(1, 10):
            message = 'message'.format(i)
            response = self.producer.send(self.kafka_topic, message.encode('utf-8'))
            # print(response)

