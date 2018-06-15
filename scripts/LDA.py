import pickle
import pandas as pd
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from nltk.stem import porter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

corpus = pickle.load(open("corpus.pkl", "rb" ))
count_vectorizer2 = CountVectorizer(ngram_range=(1, 4),
                                   stop_words='english',
                                   token_pattern="\\b[a-z][a-z]+\\b",
                                   lowercase=True,
                                   max_df = 0.6)

X = count_vectorizer2.fit_transform(corpus)

n_topics = 50
n_iter = 10
lda = LatentDirichletAllocation(n_topics=n_topics,
                                max_iter=n_iter,
                                random_state=42,
                               learning_method='online')
LDA_X = lda.fit_transform(X)

with open('LDA_X .pkl', 'wb') as picklefile:
        pickle.dump(LDA_X , picklefile)
