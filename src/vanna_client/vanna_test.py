# -*- coding:utf-8 -*-

"""
@date: 2025/5/20 上午11:01
@summary:
"""

import chromadb
from openai import OpenAI
from vanna.openai.openai_chat import OpenAI_Chat
from vanna.deepseek.deepseek_chat import DeepSeekChat
from vanna.chromadb import ChromaDB_VectorStore
from vanna.flask import VannaFlaskApp
from vanna_client.onnx_mini_lm_l6_v2 import ONNXMiniLM_L6_V2



base_url = "http://xxx/v1"
model_name = 'xx'
api_key = 'xx'
db_path = '/media/mesie/a1d6502f-8a4a-4017-a9b5-3777bd223927/model/vanna/db3'
model_path = '/media/mesie/a1d6502f-8a4a-4017-a9b5-3777bd223927/model/vanna/chroma/onnx_models/all-MiniLM-L6-v2/onnx'




embedding_function = ONNXMiniLM_L6_V2(model_path=model_path)

# chroma_client = chromadb.PersistentClient(path=db_path)
#
# chroma_client.get_or_create_collection(
#             name="documentation",
#             embedding_function=embedding_function
#         )

client = OpenAI(
    api_key=api_key,
    base_url=base_url,
)

class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, client=None, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, client=client, config=config)


config = {
    "model": model_name,
    "path": db_path,
    "language": "chinese",
    "embedding_function": embedding_function

}
vn = MyVanna(client=client, config=config)

vn.connect_to_postgres(host='xxx', dbname='xx', user='postgres', password='postgres', port=5432)
df_information_schema = vn.run_sql("SELECT * FROM INFORMATION_SCHEMA.COLUMNS")
plan = vn.get_training_plan_generic(df_information_schema)

vn.train(ddl="""""")


if __name__ == '__main__':
    app = VannaFlaskApp(vn, title="欢迎来到xxxAI")
    app.run()
