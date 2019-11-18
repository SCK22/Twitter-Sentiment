# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
import json
from textblob import TextBlob
import os
# Import the necessary package to process data in JSON format
import sys
import json
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud, STOPWORDS 
import nltk
from nltk.probability import FreqDist
import numpy as np
import plotly
import plotly.offline as pyoff
from plotly.offline import iplot, plot
import plotly.graph_objs as go

from plot_sentiment_distribution import *
from get_data import get_data, run_multiple_processes
import multiprocessing
from multiprocessing import Process, Queue, current_process, freeze_support, Pool, SimpleQueue, Manager

##get data
keyword = sys.argv[1]
try:
    count = int(sys.argv[2])
except:
    count = 50

if __name__ == "__main__":
    print("Getting tweets for the keyword : {}".format(keyword))
    get_data(keyword,count)
    # twitter does not allow mutiple connections, I wish it did .
    # run_multiple_processes(count,get_data, keyword)
    jdata = read_data(keyword)
    created_at, corpus, polarity = generate_polarity(jdata) 
    print("Plotting sentiment for the keyword  : {}".format(keyword))
    plot_fig(keyword, created_at,corpus,polarity)

