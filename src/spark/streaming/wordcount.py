# -*- coding: utf-8 -*-
from __future__ import print_function


from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

def word_count(ssc, brokers, topic):
    """"""
    kvs = KafkaUtils.createStream(ssc, brokers, "spark-streaming-consumer", {topic: 0})
    lines = kvs.map(lambda x: x[1])
    counts = lines.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
    counts.pprint()

if __name__ == '__main__':

    sc = SparkContext(appName="WordCount")
    #
    ssc = StreamingContext(sc, 2)
    brokers = "localhost:9092"
    topic = "test"
    word_count(ssc, brokers, topic)

    ssc.start()
    ssc.awaitTermination()
    """
     bin/spark-submit --jars jars/spark-streaming-kafka-0-8-assembly_2.11-2.1.0.jar /Users/t/python/big_data_framework/src/spark/streaming/wordcount.py
    """
