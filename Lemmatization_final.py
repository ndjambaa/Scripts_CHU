#!/usr/bin/env python
# coding: utf-8

# In[106]:


import spacy
import os
inputFileName = '.\Text_corpus.csv'
outputFileName = inputFileName[:-4]+'-LEMMATIZED.csv'
#if os.path.exists(outputFileName):
#    os.remove(outputFileName)

outputFile = open(outputFileName, 'a')
nlp = spacy.load('en_core_web_sm')    #first, execute python -m spacy download en
# it performs a reasonably large download
with open(inputFileName , 'r') as fp:
    line = fp.readline()
    while line:
        line = line.lower()  #optional extra formatting
        #line = line.replace('xxx ','') #optional extra cleaning - you can repeat this line as many times as needed
        list_of_lemmas = nlp(line)
        lemmatized_line=""
#decode('utf8') is optional, only if you are having problems with thecharacter set
        for word in list_of_lemmas:
            lemmatized_line += word.lemma_ + ' '
        #line = line[:-1].encode("ascii", "ignore")   #toss off last
#extra white space and force output to ascii, in case it is not alreadylike that
        outputFile.write(lemmatized_line+'\n')
        line = fp.readline() #next input line
outputFile.close()
#TAIL CLEANING BASED ON WORD FREQUENCY
import operator
import math

if __name__ == '__main__':
    mapa = {}
    with open(inputFileName) as fp:
        line = fp.readline()
        while line:
            words = line.split()
            for word in words:
                if word in mapa:   # Word already in the dictionary
                    mapa[word] = mapa[word] + 1
                else:
                    mapa[word] = 1
            line = fp.readline() #next input line
    outputFile.close()
    #word frequency is ready - now select tail words to toss of
    sorted_list = sorted(mapa.items(), key=operator.itemgetter(1))   #ahash cannot be sorted, we create a sorted list
    n_words = len(sorted_list)
    tails_off_list = sorted_list[math.floor(n_words*0.025):(n_words-math.floor(n_words*0.025)+1)]
#slices the dictionary
    #WRITE trimmed_list TO AN INCLUSION FILE
    #PROCESS CSV FILE EXCLUDING WORDS NOT IN THE INCLUSION FILE
#//-----------------------------------------
#OPTIONAL - plot "word cloud" from the word frequency data

"""from os import path
from wordcloud import WordCloud
import matplotlib.pyplot as plt
wordcloud = WordCloud(max_font_size=40).generate(" ".join([(k + ' ') *v for k,v in mapa.items()]))
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()"""

#import numpy as np
import pandas as pd
from os import path
#from PIL import Image
#import pillow
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

df = pd.DataFrame(tails_off_list)
df.columns = ['Words', 'Frequency']

plt.figure(figsize=(150000,100000))
#df.size().sort_values(by='Frequency',ascending=False).plot.bar()
df[['Words','Frequency']].sort_values(by='Frequency',ascending=False).plot(kind='bar',stacked=True)
plt.xticks(rotation=50)
plt.xlabel("Words")
plt.ylabel("Frequency")
plt.show()
plt.savefig('Occurance_des_mots.jpg')




