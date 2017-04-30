'''Conor Campbell - CSCE 590 Final Project'''
import tweepy
import csv
import nltk
import re
import time
from nltk import word_tokenize, FreqDist, pos_tag

#twitter api keys
consumer_key = 'HoUEEtLW2jIu1tq9pCXcdDLoE'
consumer_secret = 'kptLh6iaFeABzpqSNN0m1NRDhNoSl71pzmPN4sW3e43PTbHb5Y'
access_key = '517936077-axFSxWdRqWbrqewQcE8LVwRb4WhP4aCfxS7QA206'
access_secret = 'sWXhbRuVj5Uay8w7PoROwMHABPZAnUFQZu53EQseks3I6'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

''' Function to get tweets from the specified user name.
This .user_timeline function can only get 200 total tweets,
so with this being said, we request tweets from users over
and over again until there are no tweets left using the
max_id parameter.'''
def getUserTweets(username):
    tweets = []
    try:
        newTweets = api.user_timeline(screen_name=username, count=200)
    except tweepy.TweepError:
        print("Sleeping for 15 minutes to avoid rate limit.")
        time.sleep(900)
        newTweets = api.user_timeline(screen_name=username, count=200)
    tweets.extend(newTweets)

    oldestTweetID = tweets[-1].id - 1

    while len(newTweets) > 0:
        # print("Getting tweets before " + str(oldestTweetID))
        try:
            newTweets = api.user_timeline(screen_name=username, count=200, max_id=oldestTweetID)
        except tweepy.TweepError:
            print("Sleeping for 15 minutes to avoid rate limit.")
            time.sleep(900)
            newTweets = api.user_timeline(screen_name=username, count=200, max_id=oldestTweetID)
        except StopIteration:
            break
        tweets.extend(newTweets)
        oldestTweetID = tweets[-1].id - 1
        # print(str(len(tweets)) + " tweets downloaded so far.")

    ## lets remove retweets
    removeRTTweets = []
    quoteTweet = re.compile('(.*)\“(@[A-Za-z0-9_]+:.*)')
    replyTweet = re.compile('(.*)(@[A-Za-z0-9]+:.*)')
    for tweet in tweets:
        ## retweet tweet
        if not tweet.text.startswith("RT"):
            quoteResult = re.match(quoteTweet, tweet.text)
            replyResult = re.match(replyTweet, tweet.text)
            ## quote tweet, get what user says
            if quoteResult:
                tweet.text = quoteResult.group(1)
            ## reply tweet, get what user says
            if replyResult:
                tweet.text = replyResult.group(1)
            removeRTTweets.append(tweet)
        else:
            pass

    return removeRTTweets

'''Function to read the created csv file which
contains the names and twitter handles of users.'''
def readCSV(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        twitterList = list(reader)
    return twitterList

'''This function gets the most common words from
the tweets of a user using nltk.'''
def getMostCommonWords(allTweets):
    regex = re.compile('[^\w ]')
    string = ''
    for tweet in allTweets:
        string +=  (" " + tweet.text)
    string = string.lower()
    string = regex.sub('', string)
    tokens = pos_tag(word_tokenize(string))
    tokens = cleanUpPosTags(tokens)
    # print(tokens)
    fdist = FreqDist(tokens)
    return fdist.most_common(100)

'''This function eleminates words from tweets such as prepositions,
to, DT's, IN, and conjuctions.'''
def cleanUpPosTags(tokens):
    newTokens = []
    for index, element in enumerate(tokens):
        # if element[1] != 'TO' and element[1] != 'PRP' and element[1] != 'DT' and element[1] != 'PRP$' and element[1] != 'IN' and element[1] != 'CC' and element[1] != 'VBZ':
        # Currently looking for nouns or verbs
        if element[1] == 'NN' or element[1] == 'VB':
            newTokens.append(element)
    return newTokens

'''Function to output data to a csv file that is readable.'''
def createCSVFile(twitterName, mostCommonWords):
    #setup csv output
    myfile = open('./csvFiles/' + twitterName + '.csv', 'w')
    wr = csv.writer(myfile)
    wr.writerow([twitterName])

    #create new twitter name list
    for ele in mostCommonWords:
        wr.writerow([ele[0][0], ele[1]])

# Main function calls
twitterList = readCSV('twitterData.csv')
# Remove headers
twitterList = twitterList[1:]
counter = 1
for element in twitterList:
    allTweets = getUserTweets(element[1][1:])
    mostCommon = getMostCommonWords(allTweets)
    createCSVFile(element[0], mostCommon)

    print("Completed " + element[0] + "'s tweets. #" + str(counter))
    counter += 1
