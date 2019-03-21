# -*- coding: utf-8 -*-
from src.kazoo_client import Consumer
from src.kazoo_client import Producer

def main():
    ##测试生产模块
    producer = Producer("127.0.0.1", 9092, "test")
    # 测试消费者
    consumer = Consumer('127.0.0.1', 9092, "test", 'test_id')
    message = consumer.consume()
    for i in message:
        print(i.value)

if __name__ == '__main__':
    main()
