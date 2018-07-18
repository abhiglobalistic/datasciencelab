import csv
import re
from textblob import TextBlob

# Defines a list - It stores all unique tweets
tweetChecklist = [];
CSVfields = ['created_at', 'text','sentiment']


csvFile = 'AfterFinalWomansMarchTweets.csv'
csvFileNameforGeneration = 'AfterFinalSentimentWomansMarchTweets.csv'


def get_tweet_sentiment(tweet):
    '''
    Utility function to classify sentiment of passed tweet
    using textblob's sentiment method
    '''
    # create TextBlob object of passed tweet text
    analysis = TextBlob(tweet)
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'



def getAllTweets():
    AllTweets = [];
    with open(csvFile, encoding='UTF-8') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            AllTweets.append(row)

    return AllTweets


allTweets = getAllTweets()

def writeCSV(tbody,writer):
    writer.writerow(tbody)


with open(csvFileNameforGeneration, 'w', newline='',encoding='utf-8') as csvfile:
    tweetwriter = csv.DictWriter(csvfile, delimiter=',', fieldnames=CSVfields)  ## initialize the CSV
    tweetwriter.writeheader()  ## write the header of CSV
    for item in allTweets:


        #TODO Check for ratio of users

        # If tweet doesn't exist in the list  item[1]  index 1 is the text column
        if item[1] not in tweetChecklist:
            tweetChecklist.append(item[1])

            if item[1].startswith("rt"):
                csvObj = {'created_at': item[0],
                          'text': item[1][2:],
                          'sentiment':get_tweet_sentiment(item[1][2:])
                          }
                writeCSV(csvObj, tweetwriter)
            else:
                csvObj = {'created_at': item[0],
                          'text': item[1],
                          'sentiment': get_tweet_sentiment(item[1][2:])
                          }
                writeCSV(csvObj, tweetwriter)



















