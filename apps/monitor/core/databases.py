import re

import redis
from redis.exceptions import ConnectionError, ResponseError, RedisError
import pymongo
import pymysql


class RedisClient(object):
    def __init__(self, host, port, db=0, password=None):
        if password:
            self._db = redis.Redis(host=host, port=port, password=password, db=db)
        else:
            self._db = redis.Redis(host=host, port=port, db=db)

    def db_size(self):
        try:
            return self._db.dbsize()
        except (ConnectionError, RedisError, ResponseError):
            return {"Error": "check your connection"}

    def show_last_db(self):
        return self._db.config_get('databases')

    def get_keys(self):
        key_list = [key.decode('utf-8') for key in self._db.keys()]
        return key_list

    def get_type(self, key):
        return self._db.type(key).decode('utf8')

    def get_key_size(self, key):
        key_type = self.get_type(key)
        if re.search('string', key_type):
            return 1
        if re.search('list', key_type):
            return self._db.llen(key)
        if re.match('set', key_type):
            return self._db.scard(key)
        if re.search('zset', key_type):
            return self._db.zcard(key)
        if re.search('hash', key_type):
            return self._db.hlen(key)

    def list_members(self, key):
        key_type = self.get_type(key)
        if re.search('string', key_type):
            return [{'string': self._db.get(key).decode('utf8')}]
        if re.search('list', key_type):
            return [{'id': index_id + 1, 'name': item.decode('utf8')} for index_id, item in
                    enumerate(self._db.lrange(key, -100, -1))]
        if re.match('set', key_type):
            if self._db.scard(key) < 501:
                return [{'id': index_id + 1, 'name': item.decode('utf8')}
                        for index_id, item in enumerate(self._db.smembers(key))]
            else:
                return [{'Error': 'The length of redis set is too long!'}]
        if re.search('zset', key_type):
            return [{'id': index_id + 1, 'name': item.decode('utf8')} for index_id, item in
                    enumerate(self._db.zrevrange('sort_set1', -100, -1))]
        if re.search('hash', key_type):
            if self._db.hlen(key) < 501:
                return [{k.decode('utf8'): v.decode('utf8') for k, v in self._db.hgetall('hash1').items()}]
            else:
                return [{'Error': 'The length of redis hash is too long!'}]


class MongoClient(object):
    def __init__(self, host, port, username=None, password=None):
        if password:
            mongo_url = 'mongodb://%s:%s@%s:%s' % (username, password, host, port)
            self.client = pymongo.MongoClient(mongo_url)
        else:
            self.client = pymongo.MongoClient(host=host, port=port)

    def server_info(self):
        try:
            self.client.server_info()
        except Exception as e:
            return {"Error": e.args}

    def show_dbs(self):
        try:
            return self.client.list_database_names()
        except Exception as e:
            return {"Error": e.args}
        finally:
            self.client.close()

    def show_collections(self, db):
        try:
            return self.client[db].list_collection_names()
        except Exception as e:
            return {"Error": e.args}
        finally:
            self.client.close()

    def get_collection_size(self, db, collection):
        collection = self.client[db][collection]
        return collection.estimated_document_count()

    def get_collection_data(self, db, collection):
        collection = self.client[db][collection]
        result = collection.find().sort('_id', pymongo.DESCENDING)
        item_list = []
        for i in result:
            i['_id'] = str(i['_id'])
            item_list.append(i)
            if len(item_list) > 100:
                break
        return item_list


class MysqlClient(object):
    def __init__(self, host, port, user, password, database='mysql', charset='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = database
        self.charset = charset
        self.cursor = self.init_cursor(self.db)

    def init_cursor(self, database):
        connect = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                                  database=database, charset=self.charset)
        return connect.cursor()

    def show_dbs(self):
        try:
            self.cursor.execute('show databases;')
            db_list = [i[0] for i in self.cursor.fetchall()]
            return db_list
        except Exception as e:
            return {"Error": e.args}
        finally:
            self.cursor.close()

    def show_tables(self, db):
        self.cursor = self.init_cursor(db)
        try:
            self.cursor.execute('show tables;')
            table_list = [i[0] for i in self.cursor.fetchall()]
            return table_list
        except Exception as e:
            return {"Error": e.args}
        finally:
            self.cursor.close()

    def get_table_size(self, db, table):
        self.cursor = self.init_cursor(db)
        try:
            sql = "select count(*) from %s" % table
            self.cursor.execute(sql)
            return self.cursor.fetchone()[0]
        except Exception as e:
            return {"Error": e.args}
        finally:
            self.cursor.close()

    def select_data(self, db, table):
        con = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                              database=db, charset=self.charset, cursorclass=pymysql.cursors.DictCursor)
        sql = "select * from %s limit 100" % table
        try:
            with con.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                if len(result) > 1:
                    return result
                else:
                    return [{"Message": "No Data."}]
        except Exception as e:
            return [{"Error": e.args}]
        finally:
            con.close()



