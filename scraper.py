import wptools
import json
import wikipedia   
# Opening JSON file
f = open('queryResults.json',)
  
# returns JSON object as 
# a dictionary
data = json.load(f)	

#page = wptools.page
#page.get_query()

list_of_labels = []
for row in data["results"]["bindings"]:
	if len(list_of_labels) < 16:
		list_of_labels.append(row["photographer_label"]["value"])
	else: 
		break

print(list_of_labels)


for photographer in list_of_labels:    
    page = wptools.page(photographer) # create a page object
    try:
        page.get_parse() # call the API and parse the data
        if page.data['infobox'] != None:
            # if infobox is present
            infobox = page.data['infobox']
            # get data for the interested features/attributes
            data = { feature : infobox[feature] if feature in infobox else '' 
                         for feature in features }
        else:
            data = { feature : '' for feature in features }

    except KeyError:
        pass