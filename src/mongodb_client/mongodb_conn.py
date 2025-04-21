# -*- coding:utf-8 -*-

"""
@date: 2025/4/18 下午5:26
@summary: mongodb 数据库连接
"""
from bson.objectid import ObjectId
from pymongo import MongoClient
username = 'myusername'
password = 'mypassword'
host = '10.105.11.252'
port = 27017
database_name = 'fastgpt'

mongo_hosts = f"mongodb://{username}:{password}@{host}:{port}"

coll_name = 'dataset_data_texts'

client = MongoClient(mongo_hosts,
                     maxPoolSize=50,
                     minPoolSize=10,
                     maxIdleTimeMS=300000)



db = client[database_name]
collection = db[coll_name]
# # collection.insert_one({'name': 'mesie'})
# # print(collection.find_one({'name': 'mesie'}))
a = collection.find_one({'dataId': ObjectId('67d3ce0f68372eac5f22aebe')})
print(a)




