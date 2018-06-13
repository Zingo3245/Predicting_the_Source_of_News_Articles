import pickle
import pandas as pd
import numpy as np

text_w_no_nouns = pickle.load(open("text_w_no_nouns.pkl", "rb" ))

short_text = []
clear = []
for text in text_w_no_nouns:
    for part in text:
        clear.append(part[0])
    short_text.append(' '.join(clear))

with open('short_text.pkl', 'wb') as picklefile:
        pickle.dump(short_text, picklefile)
