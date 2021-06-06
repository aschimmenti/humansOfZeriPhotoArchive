import csv
from os import name, path
import json


#name_file = open('py_files/timeline_query.json')
#data = json.load(name_file)

def extract_date(row, string):
    date = ''
    if string in row.keys():  
            date = row[string]['value'][0:4]
    return date

def extract_name(row, string):
    name = ''
    if string in row.keys():  
            name = row[string]['value']
    return name

    newObj = {
                    "startDate":(extract_date(row, 'birth')),
                    "endDate": (extract_date(row, 'death')),
                    "headline": (extract_name(row, 'label')),
                    "text":"<p>Body text goes here, some HTML is OK</p>",
                    "tag":"This is Optional",
                    "classname":"optionaluniqueclassnamecanbeaddedhere",
                    "asset": {
                        "media":"http://twitter.com/ArjunaSoriano/status/164181156147900416",
                        "thumbnail":"optional-32x32px.jpg",
                        "credit":"Credit Name Goes Here",
                        "caption":"Caption text goes here"
                    }
                }
    dates.append(newObj)

def afterparty_trash(filename, data_to_write):
    with open(filename, 'w') as outfile:
        json.dump(data_to_write, outfile)

#afterparty_trash('dates.json', dates)

import csv

with open('photographers.csv') as csv_file:
    data = csv.reader(csv_file, delimiter=',')
print(data)
