# -*- coding: utf-8 -*-
from utils.mongo_connector import get_db


class MongoPipeline(object):
    def __init__(self):
        db = get_db()
        self._home_offers = db.home_offers

    def process_item(self, item, spider):
        d_item = dict(item)

        if (not self._home_offers.find_one(d_item)):
            self._home_offers.save(d_item)

        return item
