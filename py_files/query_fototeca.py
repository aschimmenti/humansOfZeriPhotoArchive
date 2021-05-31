
search_string = "Fiorentini, Pietro"
comma = ','
if comma in search_string:
    x = search_string.split(", ")
    string_to_join = str(x[1]) + ' '+ str(x[0])
print(string_to_join)

