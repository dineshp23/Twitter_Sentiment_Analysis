# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 17:34:28 2016

@author: Dinesh

Training Max Ent Model

References Taken from : https://www.ravikiranj.net/posts/2012/code/how-build-twitter-sentiment-analyzer/
"""

import re
import csv
import nltk
#import codecs
import string
import pickle
stopWords = []
tweets = []
featureList=[]
total=0
hits=0
misses=0
totalPositive=0
totalNegative=0
totalNeutral=0
correctPositive=0
correctNegative=0
correctNeutral=0
#start replaceTwoOrMore
def replaceTwoOrMore(s):
    #look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)
#end

#start getStopWordList
def getStopWordList(stopWordListFileName):
    #read the stopwords file and build a list
    stopWords = []
    stopWords.append('AT_USER')
    stopWords.append('URL')

    fp = open(stopWordListFileName, 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stopWords.append(word)
        line = fp.readline()
    fp.close()
    return stopWords
#end
def processTweet(str):
   if str is None:
       return ""
    # lower case
   low = str.lower()
   # remove URL
   url = re.sub(r"http\S+", "", low)
   # remove username
   user = re.sub(r"@\S+", "", url)
   # remove hashtag (# only)
   tag = re.sub(r"#", "", user)
   # remove ellipsis
   ellipsis = re.sub(u"\u2026", "", tag)
   # remove extra spaces
   space = " ".join(ellipsis.split())
   # remove punctuation
   exclude = set(string.punctuation)
   punc = ''.join(c for c in space if c not in exclude)
   # remove stop words
   stop = punc.split()
   final = ' '.join(word for word in stop if word not in stopWords)
   # check if preprocess result in empty string
   if (final != ''):
      return final;
#end
#start getfeatureVector
def getFeatureVector(tweet,stopWords):
    if tweet is None:
       return ""
    featureVector = []
    #split tweet into words
    words = tweet.split()
    for w in words:
        #replace two or more with two occurrences
        w = replaceTwoOrMore(w)
        #strip punctuation
        w = w.strip('\'"?,.')
        #check if the word stats with an alphabet
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
        #ignore if it is a stop word
        if(w in stopWords or val is None):
            continue
        else:
            featureVector.append(w.lower())
    return featureVector
#end
#start extract_features
def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in featureList:
        features['contains(%s)' % word] = (word in tweet_words)
    return features
#end
print("Reading Stop words")
st = open('stopwords.txt', 'r')
stopWords = getStopWordList('stopwords.txt')

#Read the tweets one by one and process it
print ("reading Training data")
ifile  = open('utf_8full_training_dataset.csv', 'rt',encoding="utf-8")
print ("Now Training feature extraction")
inpTweets = csv.reader(ifile, delimiter=',', quotechar='|')
for row in inpTweets:
    sentiment = row[0]
    if len(row)>1:
        tweet = row[1]
        if tweet is None:
            tweet=""
        else:
            processedTweet = processTweet(tweet)
            featureVector = getFeatureVector(processedTweet, stopWords)
            featureList.extend(featureVector)
            tweets.append((featureVector, sentiment));
#end loop

# Remove featureList duplicates
featureList = list(set(featureList))
# Extract feature vector for all tweets 
training_set = nltk.classify.util.apply_features(extract_features, tweets)
print ("=== Training Model ===")
#Max Entropy Classifier
MaxEntClassifier = nltk.classify.maxent.MaxentClassifier.train(training_set, 'GIS', trace=3, \
                    encoding=None, labels=None, gaussian_prior_sigma=0, max_iter = 30)
f = open('MAXENT_FullSet.pickle', 'wb')
pickle.dump(MaxEntClassifier, f)
f.close()

