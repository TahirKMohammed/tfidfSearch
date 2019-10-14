import os
from bs4 import BeautifulSoup
import nltk
import copy
from timeit import default_timer as timer

'''
================================================================================
    tf-idf-indexer
An indexer that opens a folder of files, obtains their keywords, and saves this as an index (inverted index full-text representation)

The way this works:

The index is stored as follows:
|  a  |aardvark| abacus |  abba  |  able  | ... |  zoom  |
|-----|--------|--------|--------|--------|-----|--------|
|df=34|  df=7  | df=870 |  df=90 |  df=80 |     |  df=1  |
|-----|--------|--------|--------|--------|-----|--------|
|  1  |    2   |    1   |    1   |   ..   |     |   89   |
|  8  |   51   |   11   |   23   |   12   |     |        |
| 90  |   54   |   70   |   71   |   71   |     |        |
| ..  |   ..   |   ..   |   ..   |   ..   |     |        |
|1039 |  1011  |  2933  |  800   |  983   |     |        |

The first listing in the index has the "term" we are looking for - lower case.
The second listing is the amount of documents that have this term at __least__ once.
The third listing is a list, which, in increasing order, lists the document # that has this term. This is a simple representation that should get us off the ground for tf-idf smoothly. Instead of document numbers, we will have documents sorted alphabetically (clueweb09-en0000-00-01739... etc).
================================================================================
'''

# Data declarations

'''
    index entry class
The index entry class is a single index entry which has a:
term (string)
df (integer)
doc_listings (list)

It is initialized by the __init__ method, which accepts the name of the term, and initializes df to 1, doc_listings to have the doc_name it was originally found.

The increase_df method increase df by 1.

The append_doc_name method appends a given doc_name to the doc_listings list, and sorts the list alphabetically.

The update_item method increases df and appends the doc name given.

Getters are available.
'''

class index_entry:

    def __init__(self, term):
        self.term = term
        self.df = 1
        self.doc_listings = []
        self.append_doc_name
    
    def increase_df(self):
        self.df += 1

    def append_doc_name(self, doc_name):
        self.doc_listings.append(doc_name)
        sorted(self.doc_listings)

    def update_item(self, doc_name):
        self.increase_df
        self.append_doc_name

    def get_df(self):
        return self.df
    
    def get_term(self):
        return self.term

    def get_doc_listings(self):
        return self.doc_listings

# Steps

# Open the alloted directory for documents.
inv_index = []
stop_words = set(nltk.corpus.stopwords.words('english'))
script_dir = os.path.dirname(__file__)
rel_path = "../cw09_pool/"
workfolder = os.path.join(script_dir, rel_path)
records = 0

for filename in os.listdir(workfolder):
    start = timer()
    print(filename) # this makes it easy to just look at the filename in console

    # open a single file.
    with open(os.path.join(script_dir, rel_path, filename)) as f:
        working_file = f.read()

    # markup removal.
    working_file_rm_mu = BeautifulSoup(working_file, "lxml").text

    # down-casing.
    working_file_dc = working_file_rm_mu.casefold()

    # tokenization.
    working_file_tk = nltk.tokenize.word_tokenize(working_file_dc)

    # stop word removal.

    working_file_filtered = []

    for w in working_file_tk:
        if w not in stop_words:
            working_file_filtered.append(w)

    # now we have a list (working_file_filtered) which has the list of ALL unique words in this document.

    '''
        next step: Creation of the data structure.

    With this we now build our list of documents. We use the index_entry class and an array called inv_index.

    Flow:
    Parse through the working_file_filtered list structure.
    For each token:
        if the token is in inv_index:
            token.update_item
        else:
            inv_index.append(token)

    The inverted index is sorted in place by calling the sort function, using lambda (safe but slow).
    inv_index.sort(key=lambda index_item: index_item.term)

    '''

    for token in working_file_filtered:
        flag = 1
        for entry in inv_index:
            if token == entry.term:
                entry.update_item(filename)
                flag = 0
        if flag == 1: # we didn't find an entry
            new_entry = index_entry(token)
            inv_index.append(copy.deepcopy(new_entry))
            # sort the index
            inv_index.sort(key=lambda index_item: index_item.term)

    # At the end of this we now have at least one entry in the inv_index. And, we can continue to parse through more files. Let's run it (without anything cool happening) and see what happens

    # Close the alloted directory for documents.
    f.close()
    end = timer()
    records += 1
    print("\tTime elapsed:{}, documents parsed so far:{}".format(end-start, records))

exit()
