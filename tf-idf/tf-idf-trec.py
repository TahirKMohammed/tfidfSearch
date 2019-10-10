'''
Beginner code that computes tf/idf for a set of documents (Corpus) and their related queries (topics).
'''
import os
from bs4 import BeautifulSoup
import nltk

stop_words = set(nltk.corpus.stopwords.words('english'))
script_dir = os.path.dirname(__file__)
rel_path = "../sample.xml"
workfolder = os.path.join(script_dir, rel_path)
#Opens a new file
with open(workfolder) as f:
    read_data = f.read()

print(read_data)

remove_markup = BeautifulSoup(read_data, "lxml").text

print(remove_markup)

down_case = remove_markup.casefold()

print(down_case)

tokenized = nltk.tokenize.word_tokenize(down_case)

print(tokenized)

filtered_sentence = []

for w in tokenized:
    if w not in stop_words:
        filtered_sentence.append(w)

print(filtered_sentence)

#tf-idf module: Term frequency per document/document basis.

word_frequency_pair = {"waffles":0, "breakfast":0, "fresh": 0}

for w in tokenized:
    if w == "waffles":
        waffles_frequency = waffles_frequency + 1

print(waffles_frequency)