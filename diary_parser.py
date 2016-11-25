# coding: utf-8

import csv
import os
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.diary
collection = db.trainings

filepath = os.path.dirname(os.path.abspath(__file__)) + '/data/diary_14.09.2016.csv'

with open(filepath, 'r') as csvfile:
    datareader = csv.reader(csvfile, delimiter=";")
    train_number = 0
    data = []
    for row in datareader:
        if datareader.line_num == 1:
            continue

        if len(row[0]) > 0:  # new row
            train_number += 1
            data.append({'number': train_number, 'date': row[1], 'note': row[2].strip(), 'data': []})
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

