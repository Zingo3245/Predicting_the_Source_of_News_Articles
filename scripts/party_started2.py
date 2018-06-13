import pickle
import pandas as pd
import numpy as np
import nltk
from nltk.tag import pos_tag

clean_text = pickle.load(open("clean_text.pkl", "rb" ))

def drop_nouns(text_list):
    no_nouns = []
    cleaned_text = []
    all_nouns = ['NN' or 'NNS' or 'NNP' or 'NNPS']
    for x in text_list:
        words=pos_tag(word_tokenize(x))
        werdz = [s for s in words if s[-1] != 'NN']# or 'NNS' or 'NNP' or 'NNPS']
        werdz = [s for s in werdz if s[-1] != 'NNS']
        werdz = [s for s in werdz if s[-1] != 'NNP']
        werdz = [s for s in werdz if s[-1] != 'NNPS']
        werdz = [s for s in werdz if s[-1] != ',']
        werdz = [s for s in werdz if s[-1] != '.']
        werdz = [s for s in werdz if s[-1] != ':']
        werdz = [s for s in werdz if s[-1] != 'CD']
        werdz = [s for s in werdz if s[-1] != '(']
        werdz = [s for s in werdz if s[-1] != ')']
        werdz = [s for s in werdz if s[-2] != '@']
        werdz = [s for s in werdz if s[-2] != '[']
        werdz = [s for s in werdz if s[-2] != ']']

        #check cleaned text line from function above
        no_nouns.append(werdz)
    return no_nouns

text_w_no_nouns = drop_nouns(cleaned_text)

short_text_no_nnp = []
clear = []
for text in text_w_no_nouns:
    for part in text:
        clear.append(part[0])
    short_text_no_nnp.append(' '.join(clear))
with open('short_text_no_nnp.pkl', 'wb') as picklefile:
        pickle.dump(short_text_no_nnp, picklefile)
