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
        [self.print_hit(r['_source']) for r in results['hits']['hits']]

    def print_hit(self, hit):
        print("-------------------------------")
        print("title: %s" % hit['title'].encode("utf-8"))
        print("url: %s" % hit['url'])
        print("price: %s" % hit['rent_price'])
        print("available_at: %s" % hit['available_at'])
        print("address: %s" % hit['address'])

        if('dimensions' in hit.keys()):
            print("dimensions: %s" % hit['dimensions'].encode("utf-8"))

if __name__ == '__main__':
    from elasticsearch import Elasticsearch
    es = Elasticsearch([{'host': cfg.elasticsearch['host'],  'port': cfg.elasticsearch['port']}])

    _params = yaml.load(open(sys.argv[1], 'r'))
    Search(es).query(_params)
