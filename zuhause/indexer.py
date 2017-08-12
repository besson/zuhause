from utils.mongo_connector import get_db
from bson.json_util import dumps
import sys; sys.path.append('../')
import zuhause_config as cfg
import pymongo
import json

class Indexer:

    def __init__(self, db, es):
        self.__db = db
        self.__es = es
        self.__index = 'zuhause'

    def reindex(self):
        import elasticsearch.helpers

        self.__es.indices.delete(self.__index, ignore=[400, 404])
        self.__es.indices.create(self.__index, body=json.load(open('elasticsearch/mappings.json')))

        last_updated = self.__db.find().sort('updated_at',
                                pymongo.DESCENDING).limit(1)[0]['updated_at']

        def bulkDocs():

            for result in self.__db.find({'updated_at': last_updated}):
                result['id'] = str(result.pop('_id'))

                offer = {'_index': self.__index,
                         '_type': 'offer',
                         '_id': result['id'],
                         '_source': result}

                print(offer)
                yield offer

        elasticsearch.helpers.bulk(es, bulkDocs())

if __name__ == '__main__':
    from elasticsearch import Elasticsearch
    db = get_db().home_offers
    es = Elasticsearch([{'host': cfg.elasticsearch['host'],  'port': cfg.elasticsearch['port']}])

    Indexer(db, es).reindex()
