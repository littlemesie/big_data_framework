# -*- coding: utf-8 -*-
from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import json
"""
消费者模块
"""
class Consumer(object):

    def __init__(self, kafka_host, kafka_port, kafka_topic, group_id):
        self.consumer = KafkaConsumer(kafka_topic, group_id=group_id,bootstrap_servers=[str(kafka_host) + ':' + str(kafka_port)])

    def consume(self):
        for message in self.consumer:
            print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                                 message.offset, message.key,
                                                 message.value))
if __name__ == '__main__':
    c = Consumer('localhost',9042,'user-event','user-event-tes')
    c.consumer()