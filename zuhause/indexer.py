from utils.mongo_connector import get_db
from elasticsearch import Elasticsearch
from bson.json_util import dumps
import sys; sys.path.append("../")
import zuhause_config as cfg


class Indexer:

    def __init__(self):
        self.__db = get_db()
        self.__client = Elasticsearch([{'host': cfg.elasticsearch.host, 'port': cfg.elasticsearch.port}])

    def index(self):
        for offer in self.__db.home_offers.find({"updated_at": "2017-01-28"}):
            offer.pop("_id")
            self.__client.index(index="zuhause", doc_type='offer', body=dumps(offer))

Indexer().index()
