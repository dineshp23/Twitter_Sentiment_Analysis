# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 17:33:47 2016

@author: Dinesh
Classifying based on trained Maximum Entropy Model

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
ifile  = open('utf_8full_training_dataset.csv', 'rt',encoding="utf-8")
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

f = open('MaxEnt_FullSet.pickle', 'rb')
MaxEntClassifier = pickle.load(f)
f.close()
print ("reading Test data")
testFile  = open('utf_8training_neatfile_2.csv', 'rt',encoding="utf8")
print ("classifyin test data")
testTweets = csv.reader(testFile, delimiter=',', quotechar='|')
for row in testTweets:
    total=total+1
    sentiment = row[0]
    
    #sentiment.decode("utf-8")
    if len(row)>1:
        tweet = row[1]
        if tweet is None:
            tweet=""
        else:
                testTweet = processTweet(tweet)
    
                processedTestTweet= processTweet(testTweet)
                result = MaxEntClassifier.classify(extract_features(getFeatureVector(processedTestTweet,stopWords)))
                #print(result)
                if result == '"positive"':
                    totalPositive=totalPositive+1
                    if sentiment[6:]=='"positive"'or sentiment=='"positive"':
                        correctPositive+=1
                        hits+=1
                    else:
                        misses+=1
                elif result=='"neutral"':
                    totalNeutral++1
                    if sentiment[6:]=='"neutral"'or sentiment=='"neutral"':
                        correctNeutral+=1
                        hits+=1
                    else:
                        misses+=1
                elif result=='"negative"':
                    totalNegative+=1
                    #if sentiment=='\ufeff"negative"' or sentiment=='"negative"':
                    if sentiment[6:]=='"negative"' or sentiment=='"negative"':
                        correctNegative+=1
                        hits+=1
                    else:
                        misses+=1
    
            
#end loop
#print informative features
#print (MaxEntClassifier.show_most_informative_features(10))
print ("Total Tweets:",total)
print ("Correct Predictions:",hits)
print ("Incorrect Predictions:",misses)
print ("Total Positive:",totalPositive)
print ("Total Negatives:",totalNegative)
print ("Total Neutral:",totalNeutral)
