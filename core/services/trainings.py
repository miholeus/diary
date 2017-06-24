# coding: utf-8


from config.settings.production import MONGO_HOST, MONGO_PORT
from pymongo import MongoClient
client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client.diary
collection = db.trainings


class Training:
    """
    Получение списка дат тренировок
    """
    def get_dates(self, user_id):
        min_date = collection.aggregate([{'$group': {'_id': "$id", 'date': {'$min': "$date"}}}])
        max_date = collection.aggregate([{'$group': {'_id': "$id", 'date': {'$max': "$date"}}}])
        return {'min': list(min_date)[0].get('date'), 'max': list(max_date)[0].get('date')}
