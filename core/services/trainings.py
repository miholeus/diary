# coding: utf-8

import calendar


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
        """

        :type user_id: int
        """
        min_date = collection.aggregate([{'$group': {'_id': "$id", 'date': {'$min': "$date"}}}])
        max_date = collection.aggregate([{'$group': {'_id': "$id", 'date': {'$max': "$date"}}}])
        return {'min': list(min_date)[0].get('date'), 'max': list(max_date)[0].get('date')}
    """
    Получение последовательности месяцев по датам
    """
    def get_months_sequences(self, date_start, date_end):
        """

        :param date_end: datetime.datetime
        :type date_start: datetime.datetime
        """
        years = date_end.year - date_start.year
        months = []
        for year in range(years+1):
            start = date_start.month if year == 0 else 1
            end = date_end.month if year == years else 12
            for month in range(start, end + 1):
                months.append(calendar.month_name[month])
        return months
