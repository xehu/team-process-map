import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk import tokenize
nltk.download('stopwords')
nltk.download('wordnet')
stopword = list(stopwords.words('english'))

from nltk.stem import WordNetLemmatizer  
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
from pprint import pprint
from scipy.spatial.distance import cosine

import gensim.corpora as corpora
from gensim.models import CoherenceModel
from gensim.utils import simple_preprocess
from gensim.models.ldamodel import LdaModel

def get_info_diversity(df):

    processed_data = df['message'].apply(preprocessing).tolist()

    mapping = corpora.Dictionary(processed_data)
    full_corpus = [mapping.doc2bow(text) for text in processed_data]

    lda = LdaModel(corpus=full_corpus, id2word=mapping, num_topics=10)

    topics = [lda.get_document_topics(bow) for bow in full_corpus]

    ID = calculate_information_diversity(topics, 10)
    return ID

def preprocessing(data):
        le=WordNetLemmatizer()
        word_tokens=word_tokenize(data.lower())
        tokens=[le.lemmatize(w) for w in word_tokens if w not in stopword and len(w)>3]
        return tokens

def calculate_information_diversity(doc_topics, num_topics):
        topic_matrix = []
        for doc in doc_topics:
            topic_dist = np.zeros(num_topics)
            for topic, prob in doc:
                topic_dist[topic] = prob
            topic_matrix.append(topic_dist)
        topic_matrix = np.array(topic_matrix)
        
        mean_topic_vector = np.mean(topic_matrix, axis=0)
        squared_cosine_distances = [(1 - cosine(doc, mean_topic_vector))**2 for doc in topic_matrix]
        ID = np.sum(squared_cosine_distances) / len(squared_cosine_distances)
        return ID