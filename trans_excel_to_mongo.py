# -*- coding:utf-8 -*-

import xlrd
import pymongo


class IsoMongoCon:
    def __init__(self, host='localhost', port=27017, db='movies', collection='movie_manager'):
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

def insert_data_to_mongo():
    data = xlrd.open_workbook('movies.xls')
    table = data.sheet_by_index(0)

    print(table.nrows)
    print(table.ncols)

    col_num_to_key = {}

    insert_mongo_data = {}

    with IsoMongoCon() as movie_collection:
        print('--------- collecting data from xls ---------')
        for row_number in range(table.nrows):
            print('--- reding data ---')
            for col_num in range(table.ncols):
                cell_value = table.cell(row_number, col_num).value
                if col_num == 0 and row_number != 0:
                    movie_url = table.hyperlink_map.get((row_number, 0)).url_or_path
                elif row_number == 0:
                    col_num_to_key[col_num] = cell_value
                    continue
                insert_mongo_data[col_num_to_key[col_num]] = cell_value
                insert_mongo_data['hyperlink'] = movie_url
                
            if row_number != 0:
                for key, value in insert_mongo_data.items():
                    print(u'{} -> {}'.format(key, value))
                movie_collection.insert(insert_mongo_data)
                insert_mongo_data = {}
                print('--- insert end ---')


if __name__ == "__main__":
    insert_data_to_mongo()
