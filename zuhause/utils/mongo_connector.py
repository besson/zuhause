import pymongo
import sys; sys.path.append('../')
import zuhause_config as cfg

def get_db():
    client = pymongo.MongoClient(cfg.mongodb['host'], cfg.mongodb['port'])
    return client.zuhause
