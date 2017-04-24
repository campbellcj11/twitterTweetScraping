import tweepy
import csv
import nltk
import re
from nltk import word_tokenize, FreqDist, pos_tag

#twitter api keys
consumer_key = 'HoUEEtLW2jIu1tq9pCXcdDLoE'
consumer_secret = 'kptLh6iaFeABzpqSNN0m1NRDhNoSl71pzmPN4sW3e43PTbHb5Y'
access_key = '517936077-axFSxWdRqWbrqewQcE8LVwRb4WhP4aCfxS7QA206'
access_secret = 'sWXhbRuVj5Uay8w7PoROwMHABPZAnUFQZu53EQseks3I6'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

def getUserTweets(username):
    tweets = []
    newTweets = api.user_timeline(screen_name = username,count=200)
    tweets.extend(newTweets)

    oldestTweetID = tweets[-1].id - 1

    while len(newTweets) > 0:
        print("Getting tweets before " + str(oldestTweetID))
        newTweets = api.user_timeline(screen_name=username, count=200, max_id=oldestTweetID)
        tweets.extend(newTweets)
        oldestTweetID = tweets[-1].id - 1
        print(str(len(tweets)) + " tweets downloaded so far.")

    return tweets

def readCSV(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        twitterList = list(reader)
    return twitterList

def getMostCommonWords(allTweets):
    string = ''
    for tweet in allTweets:
        string +=  (" " + tweet.text)
    string = string.lower()
    string = regex.sub('', string)
    print(string)
    tokens = pos_tag(word_tokenize(string))
    tokens = cleanUpPosTags(tokens)
    print(tokens)
    fdist = FreqDist(tokens)
    print(fdist.most_common(25))

def cleanUpPosTags(tokens):
    for element in tokens:
        if element[1] == 'TO' or element[1] == 'PRP'

twitterList = readCSV('twitterData.csv')
twitterList = twitterList[1:]
regex = re.compile('[^\w ]')
for element in twitterList:
    allTweets = getUserTweets(element[1][1:])
    getMostCommonWords(allTweets)
