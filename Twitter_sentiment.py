
# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
import json
from textblob import TextBlob
import sys 
import os

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '2292823831-oc3IkFiWRRSDWF3y7oQGQmp98lirlFWFYN4cOsJ'
ACCESS_SECRET = 'rE7H82BpbVAUZ7P1etFp0wisaMMMK5dPI2VgzG7PNfh6t'
CONSUMER_KEY = 'LHKl0287eImXDKhS9E7TOQKAV'
CONSUMER_SECRET = 'Uo2gmSpguDMUANlfDf0elnCVG4o6F1tblpu0gPAmSO3g09m4f4'
oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
import os

keyword = sys.argv[1]
# os.chdir('your_directory_here')
# Initiate the connection to Twitter Streaming API
twitter_stream = TwitterStream(auth=oauth)

# Get a sample of the public data following through Twitter
iterator = twitter_stream.statuses.filter(track=keyword,language="en")
## enter the number of tweets you want to load (remember there are limits that twitter api imposes on number of tweets that can be accessesed)
tweet_count = 10000

if os.path.isfile('tweets_{}.txt'.format(keyword)):
    os.remove('tweets_{}.txt'.format(keyword))

for tweet in iterator:
    tweet_count -= 1
    with open('tweets_{}.txt'.format(keyword), 'a') as f:
         f.write(json.dumps(tweet))
         f.write('\n')   
    if tweet_count <= 0:
        break 
