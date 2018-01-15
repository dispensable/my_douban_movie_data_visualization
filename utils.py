# -*- coding:utf-8 -*-

import pymongo

class MongoCon:
    def __init__(self, host='localhost', port=27017, 
                    db='movies', collection='movie_manager'):
        self.host = host
        self.port = port
        self.db = db
        self.collection = collection

    def __enter__(self):
        client = pymongo.MongoClient(self.host, self.port)
        self.client = client
        db = client.get_database(self.db)
        self.db = db
        self.collection = db.get_collection(self.collection)

        if self.collection:
            return self.collection
        else:
            return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()
        if not exc_tb:
            return False