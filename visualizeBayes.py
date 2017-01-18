import sys
import decimal
import re
import string
from sets import Set

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
stopwords = Set(['rt', 'mt', 'fav'])
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

topPosProb = dict()
topNegProb = dict()
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

   topPosProb.update( {s : probPos } )
   topNegProb.update( {s : probNeg } )


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
fRun = open('crawlTrump.csv', 'r')
runPos = 0
runNeg = 0
runNeu = 0
for tweetTest in fRun:
   tweetClean = preprocess( tweetTest[tweetTest.find(',') : tweetTest.find(',', tweetTest.find(',')+1)] )
   result = naiveBayes( tweetClean )
   if (result == "positive"): runPos += 1
   elif (result == "negative"): runNeg += 1
   else: runNeu += 1

print "\n Top 3 Positive Tweets: "
i = 0
for w in sorted(topPosProb, key=topPosProb.get, reverse=True):
   print w
   i += 1
   if i is 3: break

print "\n Top 3 Negative Tweets: "
i = 0
for w in sorted(topNegProb, key=topNegProb.get, reverse=True):
   print w
   i += 1
   if i is 3: break

