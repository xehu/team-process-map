import numpy as np
import pandas as pd
import scipy.stats as stats
import nltk
import csv
from nltk.corpus import stopwords

# Get the z-score of each message at the chat level: compute z-score for each message
'''
@param chat_row = one row/utterance of data
@param col_name = the name of the col for z score calculation.It will be the positive words count
@return z score of positive words at a chat level
'''
def chat_pos_zscore(df,on_column):

    #get the list of positive words
    with open("positive_affect.txt", "r") as f1:
        poswordslist = f1.read().split()

    with open("nltk_english_stopwords.txt", "r") as f2:
        stop_words = f2.read().split()

    df['stop_words'] = len([word for word in df[on_column].split() if word.lower() in stopwords])
    df['total_pos_words'] = len([word for word in df[on_column].split() if word.lower() in poswordslist])

    #Trying to group real positive words by each chat
    df['pos_words_counts'] = df['total_pos_words']-df['stop_words']
    return stats.zscore(df['pos_words_counts'])

#Test for positivity z-score
data = {
    "name": ["you are a bad person","You are a happy, joyful, lovely person"]
}

df = pd.DataFrame(data)

chat_pos_zscore(df,'name')
print(df['chat_pos_zscore'])