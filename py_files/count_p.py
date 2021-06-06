import json

name_file = open('./properties.json') 
data = json.load(name_file)

# initializing dict to store frequency of each element
elements_count = []
# iterating over the elements for frequency
for row in data['results']['bindings']:
   element = row['p']['value']
   elements_count.append(element)
print(elements_count)

import collections
counter=collections.Counter(elements_count)
print(counter)
print(len(counter))


def afterparty_trash(filename, data_to_write):
    with open(filename, 'w') as outfile:
        json.dump(data_to_write, outfile)

afterparty_trash('properties_count.json', counter)
{'http://www.wikidata.org/wiki/Property:P921': 45, 
'https://w3id.org/artchives/hasSubjectArtist': 10, 
'https://w3id.org/artchives/hasSubjectPeople': 10, 
'https://w3id.org/artchives/hasScopeAndContentSubject': 8, 
'https://w3id.org/artchives/hasSubjectPeriod': 7, 
'https://w3id.org/artchives/hasSubjectObject': 6, 
'https://w3id.org/artchives/hasSubjectGenre': 5, 
'http://www.wikidata.org/wiki/Property:P275': 2, 
'https://w3id.org/artchives/hasAggregator': 2, 
'https://w3id.org/artchives/hasCataloguingStandard': 2, 
'http://www.wikidata.org/wiki/Property:P973': 2, 
'http://www.wikidata.org/wiki/Property:P170': 1, 
'https://w3id.org/artchives/hasAccessConditions': 1, 
'https://w3id.org/artchives/hasMainObjectType': 1, 
'https://w3id.org/artchives/hasOtherObjectType': 1, 
'http://www.wikidata.org/wiki/Property:P1436': 1,
'http://www.wikidata.org/wiki/Property:P217': 1, 
'https://w3id.org/artchives/hasHistoricalNotes': 1, 
'https://w3id.org/artchives/hasNotesOnScopeAndContent': 1, 
'https://w3id.org/artchives/hasNotesOnSystemOfArrangement': 1, 
'https://w3id.org/artchives/hasAcquisitionType': 1, 
'https://w3id.org/artchives/hasNotesOnFindingAid': 1, 
'https://w3id.org/artchives/hasOtherNotes': 1, 
'http://www.wikidata.org/wiki/Property:P127': 1, 
'http://www.wikidata.org/wiki/Property:P793': 1, 
'http://www.wikidata.org/wiki/Property:P485': 1, 
'http://www.wikidata.org/wiki/Property:P1319': 1, 
'http://www.wikidata.org/wiki/Property:P1326': 1, 
'http://www.wikidata.org/wiki/Property:P571': 1, 
'https://w3id.org/artchives/hasNotesOnOtherNuclei': 1, 
'https://w3id.org/artchives/hasFirstLink': 1, 
'https://w3id.org/artchives/hasSecondLink': 1, 
'http://www.w3.org/1999/02/22-rdf-syntax-ns#type': 1, 
'http://www.w3.org/2000/01/rdf-schema#comment': 1, 
'http://www.w3.org/2000/01/rdf-schema#label': 1}