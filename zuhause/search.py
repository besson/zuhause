# -*- coding: utf-8 -*-
from utils.mongo_connector import get_db
from bson.json_util import dumps
from search.query_builder import QueryBuilder

import sys; sys.path.append('../')
import zuhause_config as cfg
import pymongo
import json
import yaml
import sys

class Search:

    def __init__(self, es):
        self.__es = es
        self.__index = 'zuhause'

    def query(self, _params):
        es_query = QueryBuilder(_params).build()
        results = es.search(index='zuhause', doc_type='offer', body=es_query)
        print("total results: %d" % results['hits']['total'])
        [self.print_hit(r['_source']) for r in results['hits']['hits']]

    def print_hit(self, hit):
        fields = ['title', 'url', 'available_at', 'address', 'dimensions']

        print("-------------------------------")

        for field in fields:
            if(field in hit.keys() and hit[field] is not None):
                print("%s: %s" % (field, hit[field].encode("utf-8")))

        print("price: %s" % hit['rent_price'])

if __name__ == '__main__':
    from elasticsearch import Elasticsearch
    es = Elasticsearch([{'host': cfg.elasticsearch['host'],  'port': cfg.elasticsearch['port']}])

    _params = yaml.load(open(sys.argv[1], 'r'))
    Search(es).query(_params)
