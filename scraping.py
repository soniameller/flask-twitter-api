import tweepy
import pandas as pd
import time
import os
from dotenv import load_dotenv
load_dotenv()
import jsonpickle
import json
import pandas as pd
import re

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

def tweets_to_df(searchQuery,maxTweets,language='',geocode=[]):
    # If results from a specific ID onwards are reqd, set since_id to that ID.
    # else default to no lower limit, go as far back as API allows
    sinceId = None

    # If results only below a specific ID are, set max_id to that ID.
    # else default to no upper limit, start from the most recent tweet matching the search query.
    max_id = -1
    tweetCount = 0

    print("Downloading max {0} tweets".format(maxTweets))

    tweets=[]

    while tweetCount < maxTweets:
        try:
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=100,lang=language,tweet_mode='extended')
                else:
                     new_tweets = api.search(q=searchQuery, count=100,lang=language,since_id=sinceId,tweet_mode='extended')
            else:
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=100,lang=language,tweet_mode='extended',
                                            max_id=str(max_id - 1))
                else:
                    new_tweets = api.search(q=searchQuery, count=100,lang=language,tweet_mode='extended',
                                            max_id=str(max_id - 1),
                                            since_id=sinceId)
            if not new_tweets:
                print("No more tweets found")
                break
            for tweet in new_tweets:
                tweets.append(tweet._json)
            tweetCount += len(new_tweets)
            print("Downloaded {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id
        
        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            break

    print ("Downloaded {0} tweets".format(tweetCount))
    return pd.DataFrame(tweets)

def get_full_text(df):
  df['condition'] = df['retweeted_status'].isna()
  df['full_text'] = df.apply(lambda x: x.full_text if (x.condition == True) else x.retweeted_status['full_text'] , axis = 1)
  df.drop('condition', inplace=True,axis=1)
  return df

def get_top_tweets(df,top_nb):
    sorted_tweets = df.sort_values(by='retweet_count', ascending=False).full_text

    top = []

    for tweet in sorted_tweets:
        while len(top) < top_nb  and tweet not in top:
            top.append(tweet)
    return top


# ----------- TEXT CLEANING FUNCTIONS ---------
def removeLinks(text):
    return re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', " ", text)

def removeEmojis(text):
    return text.encode('ascii', 'ignore').decode('ascii')

def removeEllipsis(text):
    return re.sub(r'\.\.[\.]*', " ", text)

def removeParens(text):
    return re.sub(r"[\(\[].*?[\)\]]", "", text)

def removeLF(text):
    text = re.sub('\n',' ', text)
    text = re.sub(' [ ]*', ' ', text)
    return text

def removeSpecialCharacters(text):
    text = re.sub('[#@?¿.,;:!¡&"`]',' ', text)
    return text
    

def df_to_clean_text(df):
    text = ''
    for tweet in df.full_text:
        text += tweet
    text = removeLinks(text)
    text = removeEllipsis(text)
    text = removeEmojis(text)
    text = removeParens(text)
    text = removeLF(text)
    text = removeSpecialCharacters(text)
    text = text.lower()
    print('Text lenght: ',len(text))
    return text