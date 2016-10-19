from utils.mongo_connector import get_db
from elasticsearch import Elasticsearch
from bson.json_util import dumps


class Indexer:

    def __init__(self):
        self.__db = get_db()
        self.__client = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    def index(self):
        for offer in self.__db.home_offers.find():
            offer.pop("_id")
            self.__client.index(index="zuhause", doc_type='offer', body=dumps(offer))

Indexer().index()