import csv
import re 
import json

def afterparty_trash(filename, data_to_write):
    with open(filename, 'w') as outfile:
        json.dump(data_to_write, outfile)

def reverse_string(string): 
    comma = ', '
    string_to_join = ''
    if comma in string: 
        x = string.split(", ")
        string_to_join = str(x[1]) + ' '+ str(x[0])
        return string_to_join
    else: 
        return string

jsondata = json.load(open('json_files/final_photographer_Q5.json'))
contributions = {}
with open('photographers.csv') as csv_file:
    data = csv.DictReader(csv_file, delimiter=',')

    for row in data:
        for result in jsondata["results"]["bindings"]:
            if row['photographer'] in result['label']['value']:
                contributions[result['label']['value']] = [row['contribution count']]


print(contributions)