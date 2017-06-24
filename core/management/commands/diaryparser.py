# coding: utf-8

import csv
import os

from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from config.settings.production import MONGO_HOST, MONGO_PORT
from pymongo import MongoClient
client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client.diary
collection = db.trainings


class Command(BaseCommand):
    help = 'Parses diary'

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+', type=str, help='Path to file')

    def handle(self, *args, **options):
        path = options['path']

        filepath = path[0]
        if not os.path.isfile(filepath):
            raise CommandError("File by path <%s> is not found" % filepath)

        with open(filepath, 'r') as csvfile:
            datareader = csv.reader(csvfile, delimiter=";")
            train_number = 0
            data = []
            for row in datareader:
                if datareader.line_num == 1:
                    continue

                if len(row[0]) > 0:  # new row
                    train_number += 1
                    print(row[1])
                    date_time = datetime.strptime(row[1].strip(), '%d.%m.%Y')
                    data.append({'number': train_number, 'date': date_time, 'note': row[2].strip(), 'data': []})
                else:
                    index = train_number-1
                    current_data = {'id': row[2], 'title': row[3].strip(), 'sets': []}
                    sets = []
                    sets_id = 1
                    for i in range(5, 29, 2):
                        if len(row[i+1]) != 0 or len(row[i]) != 0:
                            if len(row[i+1]) > 0:
                                reps = row[i+1]
                            else:
                                reps = None
                            if len(row[i]) > 0:
                                load = float(row[i].replace(",", "."))
                            else:
                                load = None
                            sets.append({'id': sets_id, 'reps': reps, 'load': load})
                        sets_id += 1
                    current_data['sets'] = sets
                    data[index]['data'].append(current_data)
            # load data in mongo
            for doc in data:
                doc_id = collection.insert_one(doc).inserted_id
                print("Inserted %s" % doc_id)

