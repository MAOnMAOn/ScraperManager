# import pymongo
#
# from ..configs import database_config as config
#
#
# class MongoOperator(object):
#     """
#     配置先暂时在代码之中写死, 后期进行迁徙, 不是很优雅,最好改为classMethod
#     """
#     def __init__(self, mongo_host=config["MONGO_HOST"], mongo_port=config["MONGO_PORT"]):
#         self.client = pymongo.MongoClient(host=mongo_host, port=mongo_port)
#         self.db = self.client[config["MONGO_PARAMS"].get('db', 'test')]
#         self.collection = self.db[config["MONGO_PARAMS"].get('collection', 'TestItem')]
#
#     def insert(self, *args):
#         """
#         A field in the database is set to unique. When this field is inserted, a duplicate error occurs.
#         :param args:
#         :return:
#         """
#         results = self.collection.insert_many(args)
#         return results.inserted_ids
#
#     def find(self, pattern, skips=0):  # params 可以为传入的一个字典，也可以为空白字典
#         """
#         $lt	  less than                 {'age': {'$lt': 20}}
#         $gt   more than	                {'age': {'$gt': 20}}
#         $lte  less than or equal to	    {'age': {'$lte': 20}}
#         $gte  greater or equal to   	{'age': {'$gte': 20}}
#         $ne	  not equal to	            {'age': {'$ne': 20}}
#         $in	  in range              	{'age': {'$in': [20, 23]}}
#         $nin  Not in range	            {'age': {'$nin': [20, 23]}}
#
#         $regex	Matching regular	            {'name': {'$regex': '^M.*'}}	Name starts with 'M'
#         $exists	Whether the attribute exists	{'name': {'$exists': True}}
#         $type	Type judgment               	{'age': {'$type': 'int'}}	    Age is of type int
#         $mod	Digital mode operation      	{'age': {'$mod': [5, 0]}}
#         $text	Text query                  	{'$text': {'$search': 'Mike'}}	Text type attribute contains Mike string
#         :param pattern:
#         :param skips:
#         :return: generator objects
#         """
#         results = self.collection.find(pattern).skip(skips)
#         for result in results:
#             if result:
#                 return results
#             else:
#                 print("Incorrect query conditions!")
#
#     def item_count(self, pattern):
#         results = self.find(pattern)
#         return results.count()
#
#     def item_sort(self, name):
#         """
#         :param name:
#         :return: generator objects
#         """
#         results = self.find({}).sort(name, pymongo.ASCENDING)
#         return (result[name] for result in results)
#
#     def update(self, condition, pattern, params):
#         results = self.collection.update_many(condition, {pattern: {params}})
#         return results.modified_count
#
#     def delete_many(self, name, params):
#         results = self.collection.delete_many({name: params})
#         return results.deleted_count
#
#
# if __name__ == '__main__':
#     MongoOperator().find({})
