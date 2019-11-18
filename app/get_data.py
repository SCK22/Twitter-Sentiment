
# # Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
import json
from textblob import TextBlob
import sys
import os
import multiprocessing
from multiprocessing import Process, Queue, current_process, freeze_support, Pool, SimpleQueue, Manager
with open("../access_tokens.json", "r") as f:
    access_dict = json.load(f)
    
# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = access_dict["access_token"]
ACCESS_SECRET = access_dict["access_token_secret"]
CONSUMER_KEY = access_dict["api_key"]
CONSUMER_SECRET = access_dict["api_secret"]
oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)


def run_multiple_processes(n_procs, func_exec, keyword):
    """Run multiple processes, as of now ,the admin id is fixed
     thanks to https://pythonprogramming.net/values-from-multiprocessing-intermediate-python-tutorial/ """
    print("run_multiple_processes called")
    q = Queue()
    processes = []
    data = []
    for _ in range(0, n_procs):
        p = Process(target=func_exec, args=(keyword,))
        processes.append(p)
    for p in processes:
        p.start()
    for p in processes:
        ret = q.get() # will block
        data.append(ret)
    for p in processes:
        p.join()
    return data


def get_data(keyword,tweet_count = 1):
    f_name = "get_data"
    print("{} called.".format(f_name))
    twitter_stream = TwitterStream(auth=oauth)

    # Get a sample of the public data following through Twitter
    iterator = twitter_stream.statuses.filter(track=keyword,language="en")
    ## enter the number of tweets you want to load (remember there are limits that twitter api imposes on number of tweets that can be accessesed)
    print("fetching {} tweets".format(tweet_count))
    for tweet in iterator:
        if tweet_count >0:
            if not os.path.exists('../data/tweets_{}.txt'.format(keyword)):
                with open('../data/tweets_{}.txt'.format(keyword), 'w') as f:
                    f.write(json.dumps(tweet))
                    f.write('\n')  
            else:
                with open('../data/tweets_{}.txt'.format(keyword), 'a') as f:
                    f.write(json.dumps(tweet))
                    f.write('\n')   
            tweet_count -= 1
            print("tweet_count : {}".format(tweet_count))
            if tweet_count == 0:
                break
    print("{} completed.".format(f_name))