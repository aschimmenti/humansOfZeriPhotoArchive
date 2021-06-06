import csv
import re 
import json

def afterparty_trash(filename, data_to_write):
    with open(filename, 'w') as outfile:
        json.dump(data_to_write, outfile)

institutions = {}

pattern = '([\w]+,)'

with open('py_files/photographers.csv') as csv_file:
    data = csv.DictReader(csv_file, delimiter=',')
    for row in data: 
        result = re.match(pattern, row['photographer'])
        if result:
            continue
        else: 
            if row['photographer'] != 'Anonimo':
                x = row['photographer'] 
                y = row['contribution count']
                institutions[x] = y

afterparty_trash('inst_contributions.json', institutions)

photographers = {}
with open('py_files/photographers.csv') as csv_file:
    data = csv.DictReader(csv_file, delimiter=',')
    for row in data: 
        result = re.match(pattern, row['photographer'])
        if result:
            x = row['photographer'] 
            y = row['contribution count']
            photographers[x] = y
        else: 
           continue

afterparty_trash('q5_contributions.json', photographers)

def total_contributions(dict):
    total = 0
    for key, value in dict.items(): 
        total = total + int(value) 
    return total 

print(total_contributions(photographers))
print(total_contributions(institutions))
