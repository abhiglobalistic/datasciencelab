import  tarfile
import simplejson as json
import sys
import os
import bz2
import re
import tweet_utils as Util
import csv
from nltk.tokenize import WordPunctTokenizer
from bs4 import BeautifulSoup


bz2FilePath = 'Coachella_Dataset/after/2016'
CSVfields = ['created_at', 'text','hashtags','username','screenname','followers_count','following_count','user_location','user_desc']

tok = WordPunctTokenizer()

pat1 = r'@[A-Za-z0-9_]+'
pat2 = r'https?://[^ ]+'
combined_pat = r'|'.join((pat1, pat2))
www_pat = r'www.[^ ]+'
negations_dic = {"isn't": "is not", "aren't": "are not", "wasn't": "was not", "weren't": "were not",
                 "haven't": "have not", "hasn't": "has not", "hadn't": "had not", "won't": "will not",
                 "wouldn't": "would not", "don't": "do not", "doesn't": "does not", "didn't": "did not",
                 "can't": "can not", "couldn't": "could not", "shouldn't": "should not", "mightn't": "might not",
                 "mustn't": "must not"}
neg_pattern = re.compile(r'\b(' + '|'.join(negations_dic.keys()) + r')\b')

def tweet_cleaner(text):
    soup = BeautifulSoup(text)
    souped = soup.get_text()
    try:
        bom_removed = souped.decode("utf-8-sig").replace(u"\ufffd", "?")
    except:
        bom_removed = souped
    stripped = re.sub(combined_pat, '', bom_removed)
    stripped = re.sub(www_pat, '', stripped)
    lower_case = stripped.lower()
    neg_handled = neg_pattern.sub(lambda x: negations_dic[x.group()], lower_case)
    letters_only = re.sub("[^a-zA-Z]", " ", neg_handled)
    # During the letters_only process two lines above, it has created unnecessay white spaces,
    # I will tokenize and join together to remove unneccessary white spaces
    words = [x for x in tok.tokenize(letters_only) if len(x) > 1]
    return (" ".join(words)).strip()

def checkDesc(tweet):
    descr = 'empty'
    if tweet['user']['description'] == None:
        return descr
    else:
        return tweet['user']['description']


def contains_word(s, w):
    return (' ' + w + ' ') in (' ' + s + ' ')

def checkHashtagForTweet(tweet):

    HashtagsList = ['coachella2017','Coachella','coachellalive','Beychella','coachellaoutfit',
                    'Coachellavalley','coachellavibes','coachellaready']

    hashtags = []
    if 'hashtags' in tweet['entities']:
        for tag in tweet['entities']['hashtags']:
            if tag['text'] in HashtagsList:
                hashtags.append(tag['text'])


                tweettext = tweet_cleaner(tweet['text'])

                csvObj = {'created_at': tweet['created_at'],
                          'text': tweettext,
                          'hashtags':hashtags,
                          'username': tweet['user']['name'],
                          'screenname': tweet['user']['screen_name'],
                          'followers_count': tweet['user']['followers_count'],
                          'following_count': tweet['user']['friends_count'],
                          'user_location': tweet['user']['location'],
                          'user_desc': checkDesc(tweet)
                          }
                print(csvObj)
                return csvObj


def writeCSV(tbody,writer):
    writer.writerow(tbody)




def reading(filepath):
    with open('AfterCoachellatweets.csv', 'w', newline='',encoding='utf-8') as csvfile:  ## open the CSV new file
        tweetwriter = csv.DictWriter(csvfile,delimiter=',', fieldnames=CSVfields) ## initialize the CSV
        tweetwriter.writeheader()  ## write the header of CSV

        for root, dirs, files in os.walk(filepath): ## read the folder
            for name in files: ## read the file
                print("PATHHH---------", os.path.join(root, name).capitalize())
                filename = os.path.join(root,name)  ## save the path of the file

                with bz2.BZ2File(filename,'r') as f:  ## read the BZ file in the path
                    for line in f:  ## read each line
                        tweet = json.loads(line) ## parse the json
                        try:
                            if tweet['created_at']:
                                if tweet['lang'] == 'en':
                                    tweetbody = checkHashtagForTweet(tweet)
                                    if tweetbody:
                                        writeCSV(tweetbody,tweetwriter)
                                        #tweetwriter.writerow(tweetbody)

                        except Exception as e:
                            continue


        
reading(bz2FilePath)
    



