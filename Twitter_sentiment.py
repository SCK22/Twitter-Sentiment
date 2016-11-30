
# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = 'token'
ACCESS_SECRET = 'token'
CONSUMER_KEY = 'token'
CONSUMER_SECRET = 'token'
oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
import os
os.chdir('your_directory_here')
# Initiate the connection to Twitter Streaming API
twitter_stream = TwitterStream(auth=oauth)

# Get a sample of the public data following through Twitter
iterator = twitter_stream.statuses.filter(track='keyword',language="en")
## enter the number of tweets you want to load (remember there are limits that twitter api imposes on number of tweets that can be accessesed)
tweet_count = 100

for tweet in iterator:
    tweet_count -= 1
    with open('tweets.txt', 'a') as f:
         f.write(json.dumps(tweet))
         f.write('\n')   
    if tweet_count <= 0:
        break 
# Import the necessary package to process data in JSON format
import json
with open('tweets.txt') as json_data:
    d = (json_data).readlines()
jdata =[]
for i in d:
    jdata.append(json.loads(i))       

from textblob import TextBlob
for i in range(len(jdata)):
    if 'text' in jdata[i]:
        tb = TextBlob(jdata[i]['text'])
        if tb.sentiment.subjectivity >0.5: # feel free to change the subjectivity level , this is related to how related the tweet is, to the key word
            if tb.sentiment.polarity > 0.5:
                print jdata[i]['text'],"\n###########positive","Score:",tb.sentiment.polarity
            elif 0 < tb.sentiment.polarity < 0.5: 
                print jdata[i]['text'],"\n###########neutral","Score:",tb.sentiment.polarity
            elif TextBlob(jdata[0]['text']).sentiment.polarity < 0 :
                print jdata[i]['text'], "\n###########negative","Score:",tb.sentiment.polarity
    
