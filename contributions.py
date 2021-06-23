import csv 
import re

def reverse_string(string): 
    comma = ', '
    string_to_join = ''
    if comma in string: 
        x = string.split(", ")
        string_to_join = str(x[1]) + ' '+ str(x[0])
        return string_to_join
    else: 
        return string

pattern = '([\d]+)'

