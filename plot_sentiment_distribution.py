# Import the necessary package to process data in JSON format
import sys
import json
from textblob import TextBlob
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

try:
    keyword = sys.argv[1]
except:
    pass
stopwords = set(STOPWORDS) 

def read_data(keyword):
    with open('tweets_{}.txt'.format(keyword)) as json_data:
        d = (json_data).readlines()
    jdata =[]
    for i in d:
        jdata.append(json.loads(i))
    return jdata
jdata = read_data(keyword)

corpus = []
polarity = []
created_at = []
for i in range(len(jdata)):
    if 'text' in jdata[i]:
        tb = TextBlob(jdata[i]['text'])        
        if tb.sentiment.subjectivity >0.5: # feel free to change the subjectivity level , this is related to how related the tweet is, to the key word
            corpus.append(jdata[i]['text'])
            created_at.append(jdata[i]['created_at'])
            polarity.append(tb.sentiment.polarity)
            # if tb.sentiment.polarity > 0.5:
            #     print (jdata[i]['text'],"\n###########positive","Score:",tb.sentiment.polarity)
            # elif 0 < tb.sentiment.polarity < 0.5: 
            #       print (jdata[i]['text'],"\n###########neutral","Score:",tb.sentiment.polarity)
            # elif TextBlob(jdata[0]['text']).sentiment.polarity < 0 :
            #     print (jdata[i]['text'], "\n###########negative","Score:",tb.sentiment.polarity)

def plot_word_cloud(corpus):
    
    df = pd.DataFrame(corpus, columns = ['text'])
    corp = " ".join(df.text.to_list()).split(" ")
    freqdist = FreqDist(corp)
    print(freqdist.most_common(20))
    wordcloud = WordCloud(width = 800, height = 800, 
                    background_color ='black', 
                    stopwords = stopwords,max_words= 20, 
                    min_font_size = 10).generate(corp)
    
    # plot the WordCloud image                        
    plt.figure(figsize = (8, 8), facecolor = None) 
    plt.imshow(wordcloud) 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 
    plt.show() 

def create_sentiment_column(polarity_val):
    if polarity_val == 0.5:
        return 'neutral'
    if polarity_val > 0.5:
        return 'positive'
    if polarity_val < 0.5:
        return 'negative'
    else:
        return 'null'

def create_csv(corpus,polarity):
    df = pd.DataFrame(zip(corpus,created_at,polarity), columns = ['text','created_at', 'polarity'])
    date_format = '%a %b %d %H:%M:%S +0000 %Y'
    df['created_at'] = pd.to_datetime(df['created_at'],format = date_format)
    df['sentiment'] = df['polarity'].apply(lambda x : create_sentiment_column(x) )
    df.to_csv("{}.csv".format(keyword),index=False)
    return df

df = create_csv(corpus,polarity)
# plot_word_cloud(corpus)

# Create traces
trace0 = go.Scatter(
    x = df['created_at'].apply(lambda x : x.minute),
    y = df['polarity'],
    mode = 'lines',
    name = 'lines'
)

data = [trace0]

plot(data)