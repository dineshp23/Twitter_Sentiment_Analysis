# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 18:23:53 2016

@author: Dinesh
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 20:07:48 2016

@author: Dinesh
"""

#import decimal
import re
import string
import csv
total=0
totalPositive=0
totalNegative=0
totalNeutral=0
totalUnknownResults=0
positiveFeatures=[]
negativeFeatures=[]
neutralFeatures=[]
posJanCount=0;
posFebCount=0;
posMarCount=0;
posAprCount=0;
posMayCount=0;
posJunCount=0;
posJulCount=0;
posAugCount=0;
posSepCount=0;
posOctCount=0;
posNovCount=0;
posDecCount=0;
posMonths=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
negMonths=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
neutralMonths=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#from sets import Set
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
        elif len(w)<4:
            continue
        else:
            featureVector.append(w.lower())
    return featureVector
def replaceTwoOrMore(s):
    #look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)
#end
def findMonthAndIncrement(s,senti):
    if(senti=="positive"):
        if (s=="Jan"):
            posMonths[0]+=1
        elif(s=="Feb"):
            posMonths[1]+=1
        elif(s=="Mar"):
            posMonths[2]+=1
        elif(s=="Apr"):
            posMonths[3]+=1
        elif(s=="May"):
            posMonths[4]+=1
        elif(s=="Jun"):
            posMonths[5]+=1
        elif(s=="Jul"):
            posMonths[6]+=1
        elif(s=="Aug"):
            posMonths[7]+=1
        elif(s=="Sep"):
            posMonths[8]+=1
        elif(s=="Oct"):
            posMonths[9]+=1
        elif(s=="Nov"):
            posMonths[10]+=1
        elif(s=="Dec"):
            posMonths[11]+=1
    elif(senti=="negative"):
        if (s=="Jan"):
            negMonths[0]+=1
        elif(s=="Feb"):
            negMonths[1]+=1
        elif(s=="Mar"):
            negMonths[2]+=1
        elif(s=="Apr"):
            negMonths[3]+=1
        elif(s=="May"):
            negMonths[4]+=1
        elif(s=="Jun"):
            negMonths[5]+=1
        elif(s=="Jul"):
            negMonths[6]+=1
        elif(s=="Aug"):
            negMonths[7]+=1
        elif(s=="Sep"):
            negMonths[8]+=1
        elif(s=="Oct"):
            negMonths[9]+=1
        elif(s=="Nov"):
            negMonths[10]+=1
        elif(s=="Dec"):
            negMonths[11]+=1
    elif(senti=="neutral"):
        if (s=="Jan"):
            neutralMonths[0]+=1
        elif(s=="Feb"):
            neutralMonths[1]+=1
        elif(s=="Mar"):
            neutralMonths[2]+=1
        elif(s=="Apr"):
            neutralMonths[3]+=1
        elif(s=="May"):
            neutralMonths[4]+=1
        elif(s=="Jun"):
            neutralMonths[5]+=1
        elif(s=="Jul"):
            neutralMonths[6]+=1
        elif(s=="Aug"):
            neutralMonths[7]+=1
        elif(s=="Sep"):
            neutralMonths[8]+=1
        elif(s=="Oct"):
            neutralMonths[9]+=1
        elif(s=="Nov"):
            neutralMonths[10]+=1
        elif(s=="Dec"):
            neutralMonths[11]+=1
        
            
            
        
# Preprocess Function
# @param: str = a string to be preprocess
def preprocess(str):
   # lower case
   #low = str.lower()
   # remove URL
   url = re.sub(r"http\S+", "", str)
   # remove username
   user = re.sub(r"@\S+", "", url)
   # remove hashtag (# only)
   tag = re.sub(r"#", "", user)
   # remove ellipsis
   ellipsis = re.sub(u"\u2026", "", tag)
   # remove extra spaces
   space = " ".join(ellipsis.split())
   # remove punctuation except emoticons
   exclude = set(string.punctuation)
   emo = {':)':'HF', '(:':'RHF', ':(':'SF', '):':'RSF'}
   for emote, placeholder in emo.iteritems():
      space = space.replace(emote, placeholder)
   punc = ''.join(c for c in space if c not in exclude)
   for emote, placeholder in emo.iteritems():
      punc = punc.replace(placeholder, emote)
   # negation
   punc = punc.replace("not ", "NOT")
   punc = punc.replace("no ", "NOT")
   # remove stop words
   stop = punc.split()
   final = ' '.join(word for word in stop if word not in stopwords)
   # check if preprocess result in empty string
   if (final != ''):
      return final;
   else:
      return '';

# Create set of stop words
stopwords = set(['rt', 'mt', 'fav'])
f = open("stopwords.txt", 'r')
for line in f:
   stopwords.update(line)

totalCount = dict()
posCount = dict()
negCount = dict()
neuCount = dict()

totalLine = 0
posLine = 0
negLine = 0
neuLine = 0
totalPos = 0
totalNeg = 0
totalNeu = 0

# Training
fTrain = open("training_dataset.csv", 'r')
for line in fTrain:
   sent = preprocess( line[:line.find(',')] )
   text = preprocess( line[line.find(','):] )
   if text is None: continue

   totalLine += 1
   if sent == "positive":
      for t in text.split(): totalPos += 1
      posLine += 1
   elif sent == "negative":
      for t in text.split(): totalNeg += 1
      negLine += 1
   else:
      for t in text.split(): totalNeu += 1
      neuLine += 1

   for t in text.split():
      if t in totalCount:
         totalCount[t] += 1
      else:
         totalCount.update( {t : 1} )

      if sent == "positive":
         if t in posCount:
            posCount[t] += 1
         else:
            posCount.update( {t : 1} )
      elif sent == "negative":
         if t in negCount:
            negCount[t] += 1
         else:
            negCount.update( {t : 1} )
      else:
         if t in neuCount:
            neuCount[t] += 1
         else:
            neuCount.update( {t : 1} )

# Naive Bayes function
# s = string to find probability
def naiveBayes(s):
   probNeg = float(negLine) / float(totalLine)
   probPos = float(posLine) / float(totalLine)
   probNeu = float(neuLine) / float(totalLine)
   # Multiply prob of each words
   # Laplace smoothing of 1
   for word in s.split():
      if word in totalCount:
         if word in posCount:
            probPos *= float(posCount[word]) / float(totalCount[word])
            #probPos *= float(posCount[word]) / float(totalPos)
         else:
            probPos *= 1 / float(totalCount[word])

         if word in negCount:
            probNeg *= float(negCount[word]) / float(totalCount[word])
            #probNeg *= float(negCount[word]) / float(totalNeg)
         else:
            probNeg *= 1 / float(totalCount[word])

         if word in neuCount:
            probNeu *= float(neuCount[word]) / float(totalCount[word])
            #probNeu *= float(neuCount[word]) / float(totalNeu)
         else:
            probNeu *= 1 / float(totalCount[word])

      if word in dNeg:
         negP = float(dNeg[word])+1
         probNeg *= negP
      elif word in dPos:
         posP = float(dPos[word])+1
         probPos *= posP


   if (probNeu > probPos and probNeu > probNeg):
      return "neutral";
   elif (probNeg > probPos and probNeg >= probNeu):
      return "negative";
   else:
      return "positive";

# Build + and - dict from file
dPos = dict()
dNeg = dict()
f = open('vader_sentiment_lexicon.txt', 'r')
for line in f:
   str = line.split('\t')
   if (str[1][0] == '-'):
      dNeg.update( {str[0]:str[1][1:]} )
   else:
      dPos.update( {str[0]:str[1]} )

# Run Naive Bayes on tweets
correct = 0;
wrong = 0;
fTest = open('crawlHurricaneMatthew.csv', 'rt')
testTweets = csv.reader(fTest, delimiter=',', quotechar='|')
for row in testTweets:
   total+=1
   if len(row)>1:
        tweetTest = row[1]
        month= row[0]
#   else:
#        totalUnknownResults+=1
   # Get expected sentiment from file
   if tweetTest is None:
            tweetTest=""
            
   else:
       tweet_words = set(tweetTest)
       features= []
       features = getFeatureVector(tweetTest,stopwords)
       tweetClean = preprocess( tweetTest[:tweetTest.find(',')] )
       #tweetClean = preprocess( tweetTest[tweetTest.find(','):] )
   # Run naive Bayes and compare with expected
       result=naiveBayes( tweetClean )
       if(result == "positive"):
           totalPositive+=1
           findMonthAndIncrement(month,"positive")
           for word in features: 
               positiveFeatures.append(word)
       elif(result == "negative"):
           totalNegative+=1
           findMonthAndIncrement(month,"negative")
           
           for word in features:
               negativeFeatures.append(word)
       elif(result == "neutral"):
            totalNeutral+=1
            findMonthAndIncrement(month,"neutral")
            
            for word in features:
               neutralFeatures.append(word)
       else:
           totalUnknownResults+=1
       if (result == ""):
           correct += 1
       else:
           wrong += 1
       
# Print #ofCorrect and #ofWrong
#print (correct, ' ', wrong)
print ('Positive:',totalPositive)
print ('Negative:',totalNegative)
print ('Neutral:',totalNeutral)
print ('Unknown:',totalUnknownResults)
print ('Total:',total)
with open('Sentiment.csv', 'wt') as csvfile:
                   spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                   spamwriter.writerow(['Positive']+[',']+[totalPositive])
                   spamwriter.writerow(['Negative']+[',']+[totalNegative])
                   spamwriter.writerow(['Neutral']+[',']+[totalNeutral])
with open('PositiveFeatures.csv', 'wt') as csvfile:
                   spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                   for w in positiveFeatures:
                       spamwriter.writerow([w])
with open('NegativeFeatures.csv', 'wt') as csvfile:
                   spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                   for w in negativeFeatures:
                               spamwriter.writerow([w]) 

                               
with open('NeutralFeatures.csv', 'wt') as csvfile:
                   spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                   for w in neutralFeatures:
                       spamwriter.writerow([w])
with open('PosMonths.csv', 'wt') as csvfile:
                   spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                   i=0
                   for w in posMonths:
                       if(i==0):
                           spamwriter.writerow([w]+[',']+['Jan'])
                           i+=1;
                       elif(i==1):
                           spamwriter.writerow([w]+[',']+['Feb'])
                           i+=1;
                       elif(i==2):
                           spamwriter.writerow([w]+[',']+['Mar'])
                           i+=1;
                       elif(i==3):
                           spamwriter.writerow([w]+[',']+['Apr'])
                           i+=1;
                       elif(i==4):
                           spamwriter.writerow([w]+[',']+['May'])
                           i+=1;
                       elif(i==5):
                           spamwriter.writerow([w]+[',']+['Jun'])
                           i+=1;
                       elif(i==6):
                           spamwriter.writerow([w]+[',']+['Jul'])
                           i+=1;
                       elif(i==7):
                           spamwriter.writerow([w]+[',']+['Aug'])
                           i+=1;
                       elif(i==8):
                           spamwriter.writerow([w]+[',']+['Sep'])
                           i+=1;
                       elif(i==9):
                           spamwriter.writerow([w]+[',']+['Oct'])
                           i+=1;
                       elif(i==10):
                           spamwriter.writerow([w]+[',']+['Nov'])
                           i+=1;
                       elif(i==11):
                           spamwriter.writerow([w]+[',']+['Dec'])
                           i+=1;    
with open('NegMonths.csv', 'wt') as csvfile:
                   spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                   i=0
                   for w in negMonths:
                       if(i==0):
                           spamwriter.writerow([w]+[',']+['Jan'])
                           i+=1;
                       elif(i==1):
                           spamwriter.writerow([w]+[',']+['Feb'])
                           i+=1;
                       elif(i==2):
                           spamwriter.writerow([w]+[',']+['Mar'])
                           i+=1;
                       elif(i==3):
                           spamwriter.writerow([w]+[',']+['Apr'])
                           i+=1;
                       elif(i==4):
                           spamwriter.writerow([w]+[',']+['May'])
                           i+=1;
                       elif(i==5):
                           spamwriter.writerow([w]+[',']+['Jun'])
                           i+=1;
                       elif(i==6):
                           spamwriter.writerow([w]+[',']+['Jul'])
                           i+=1;
                       elif(i==7):
                           spamwriter.writerow([w]+[',']+['Aug'])
                           i+=1;
                       elif(i==8):
                           spamwriter.writerow([w]+[',']+['Sep'])
                           i+=1;
                       elif(i==9):
                           spamwriter.writerow([w]+[',']+['Oct'])
                           i+=1;
                       elif(i==10):
                           spamwriter.writerow([w]+[',']+['Nov'])
                           i+=1;
                       elif(i==11):
                           spamwriter.writerow([w]+[',']+['Dec'])
                           i+=1;
with open('NeutralMonths.csv', 'wt') as csvfile:
                   spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                   i=0
                   for w in neutralMonths:
                       if(i==0):
                           spamwriter.writerow([w]+[',']+['Jan'])
                           i+=1;
                       elif(i==1):
                           spamwriter.writerow([w]+[',']+['Feb'])
                           i+=1;
                       elif(i==2):
                           spamwriter.writerow([w]+[',']+['Mar'])
                           i+=1;
                       elif(i==3):
                           spamwriter.writerow([w]+[',']+['Apr'])
                           i+=1;
                       elif(i==4):
                           spamwriter.writerow([w]+[',']+['May'])
                           i+=1;
                       elif(i==5):
                           spamwriter.writerow([w]+[',']+['Jun'])
                           i+=1;
                       elif(i==6):
                           spamwriter.writerow([w]+[',']+['Jul'])
                           i+=1;
                       elif(i==7):
                           spamwriter.writerow([w]+[',']+['Aug'])
                           i+=1;
                       elif(i==8):
                           spamwriter.writerow([w]+[',']+['Sep'])
                           i+=1;
                       elif(i==9):
                           spamwriter.writerow([w]+[',']+['Oct'])
                           i+=1;
                       elif(i==10):
                           spamwriter.writerow([w]+[',']+['Nov'])
                           i+=1;
                       elif(i==11):
                           spamwriter.writerow([w]+[',']+['Dec'])
                           i+=1;
