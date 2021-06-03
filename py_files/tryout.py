import csv
from os import path
import json
def to_text(path):
    final_text = list()
    with open(path, newline='') as csvfile:
        photographers = csv.DictReader(csvfile)
        for row in photographers:
            x = str(row['photographer']) 
            y = int(row['contribution count'])
            text = list()
            for n in range(y):
                text.append(x)
            final_text.append(' '.join(text))
    final_string = ' '.join(final_text)
    return final_string
        
def save_to_file(content, filename):
    with open(filename, 'w') as file:
        file.write(content)

#save_to_file(final_string, "cloud.txt")

import matplotlib.pyplot as pPlot
from wordcloud import WordCloud, STOPWORDS
import numpy as np
from PIL import Image
dataset = open("cloud.txt", "r").read()
def create_word_cloud(string):
   maskArray = np.array(Image.open("cloud.png"))
   cloud = WordCloud(background_color = "white", max_words = 200, mask = maskArray, stopwords = set(STOPWORDS))
   cloud.generate(string)
   cloud.to_file("wordCloud.png")
dataset = dataset.lower()
create_word_cloud(dataset)


def reverse_string(string): 
    comma = ', '
    string_to_join = ''
    if comma in string: 
        x = string.split(", ")
        string_to_join = str(x[1]) + ' '+ str(x[0])
        return string_to_join
    else: 
        return string


name_file = open('./final_photographer_Q5.json')
data = json.load(name_file)

