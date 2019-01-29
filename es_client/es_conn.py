# encoding: utf-8
from elasticsearch import Elasticsearch

class ESSearch:

    def __init__(self):
        self.es_conn = Elasticsearch(host='127.0.0.1', port=9200, timeout=60, max_retries=10, retry_on_timeout=True)

    def conn(self):
        return self.es_conn

    def ping(self, **query_params):
        return self.es_conn.ping(**query_params)

    def info(self, **query_params):
        return self.es_conn.info(**query_params)

    def create(self, index, doc_type, body, id, **query_params, ):
        """
        build create
        :param index:
        :param doc_type:
        :param id:
        :param body:
        :param query_params:
        :return:
        """
        return self.es_conn.create(index=index, doc_type=doc_type, id=id, body=body, **query_params)

    def index(self, index, doc_type, body, id=None, **query_params):
        """
        build index
        :param index:
        :param doc_type:
        :param body:
        :param id:
        :param query_params:
        :return:
        """
        return self.es_conn.index(index=index, doc_type=doc_type, body=body, id=id, **query_params)

    def search(self, index, doc_type, body):
        """
        build search
        :param index: index name
        :param doc_type: doc_type
        :param body: body
        :return: search result
        """
        return self.es_conn.search(index=index, doc_type=doc_type, body=body)

    def get(self, index, doc_type, id, params=None):
        """
        get
        :param index:
        :param doc_type:
        :param id:
        :param params:
        :return:
        """
        return self.es_conn.get(index=index, doc_type=doc_type, id=id, params=params)

    def update(self, index, doc_type, id, body=None, params=None):
        """
        update
        :param index:
        :param doc_type:
        :param id:
        :param body:
        :param params:
        :return:
        """
        return self.es_conn.update(index=index, doc_type=doc_type, id=id, body=body, params=params)

    def delete(self, index, doc_type, id, params=None):
        """
        delete
        :param index:
        :param doc_type:
        :param id:
        :return:
        """
        return self.es_conn.delete(index=index, doc_type=doc_type, id=id, params=params)

    def build_aggs_search_body(self, must_conditions, aggs_result):
        """
        build search have aggs
        :param must_conditions: must conditions
        :param aggs_result: aggs conditions
        :return: search body
        """
        search_body = {
            "size": 0,
            "query": {
                "bool": {
                    "must": must_conditions
                }
            },
            "aggs": aggs_result
        }
        return search_body

    @staticmethod
    def build_must_terms(objs):
        """
        build must term
        :param objs: must term objs
        :return: aggs body
        """
        tmp = []
        if len(objs) > 0:
            for (k, v) in objs.items():
                obj = dict()
                obj[k] = v
                obj_term = dict()
                obj_term['term'] = obj
                tmp.append(obj_term)
        return tmp

    @staticmethod
    def build_normal_aggs(aggs_field):
        """
        build normal aggs
        :param aggs_field: aggs field
        :return: aggs body
        """
        tmp = dict()
        aggs_result = dict()
        terms = dict()
        terms["field"] = aggs_field
        terms["size"] = 0
        order = dict()
        order["_count"] = "desc"
        terms["order"] = order
        aggs_result["terms"] = terms
        tmp["aggs_result"] = aggs_result
        return tmp

    @staticmethod
    def build_cardinality_aggs(cardinality_field):
        """
        build aggs of cardinality
        :param cardinality_field: field to compute cardinality
        :return: aggs body
        """
        cardinality_body = {
            "distinct_msgId": {
                "cardinality": {
                    "field": cardinality_field
                }
            }
        }
        return cardinality_body

    @staticmethod
    def build_count_aggs(count_field):
        """
        build aggs of value_count
        :param count_field: field to compute count_field
        :return: aggs body
        """
        value_count_body = {
            "count_of_field": {
                "value_count": {
                    "field": count_field
                }
            }
        }
        return value_count_body

    @staticmethod
    def build_min_aggs(min_field):
        """
        build aggs of min
        :param min_field: field to compute min value
        :return: aggs body
        """
        min_body = {
            "min_sms_time": {"min": {"field": min_field}}
        }
        return min_body



    def build_stu_score_body(self, stu_no):
        search_body = {
            "size": 0,
            "query": {
                "term": {
                    "stu_no": {
                        "value": stu_no
                    }
                }
            },
            "aggs": {
                "last_request_time": {
                    "max": {
                        "field": "@timestamp"
                    }
                }
            }
        }
        return search_body


if __name__ == '__main__':
    """简单的使用"""
    es = ESSearch()
    stu_no = 123456
    es_score_body = es.build_stu_score_body(stu_no)
    # print(es_score_body)
    # result = es.index(index="stuscore", doc_type="logs", body=es_score_body)

    result = es.delete(index="stuscore", doc_type="logs", id='iMkOmGgBUodGmVpXdKT0', params='')
    print(result)
    # result = es.search(index="stuscore", doc_type="logs", body='')
    # print(result)
    #
    # scores = []
    # for hit in result['hits']['hits']:
    #     scores.append(str(hit['_score']['data']['stuScore']))
    # print(scores)
