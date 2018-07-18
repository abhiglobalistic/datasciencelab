import nltk
nltk.download('punkt')
import pandas as pd
from textblob import TextBlob
from textblob import Word

train = pd.read_csv('DuringFinalSentimentWomansMarchTweets.csv')


# Remove rare words --------
def removeRareWords(data):
    freq = pd.Series(' '.join(data['text']).split()).value_counts()[-10:]
    freq = list(freq.index)
    data['text'] = data['text'].apply(lambda x: " ".join(x for x in x.split() if x not in freq))
    print(data['text'].head())
# Remove rare words --------


def lemmatize(data):
    data['text'] = data['text'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))
    print(data['text'].head())

def fetchBigrams(data):
    words = TextBlob(data['text'][0]).ngrams(2)
    print(words)


fetchBigrams(train)
