# Add path of 2 libraries: oauth2 and httplib2
import sys
sys.path.append("/home/csmajs/cthan004/cs235/python-oauth2")
sys.path.append("/home/csmajs/cthan004/cs235/httplib2/python2")

import oauth2 as oauth
import json
import re
import string
from sets import Set
import time

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

# Initialize keys
consumerKey = "";
consumerSecret ="";
accessToken = "";
accessTokenSecret = "";

# Verify Keys
consumer = oauth.Consumer(key=consumerKey, secret=consumerSecret)
access = oauth.Token(key=accessToken, secret=accessTokenSecret)
client = oauth.Client(consumer, access)

fWrite = open('crawlHurricane2.csv', 'a')

#id = 803702181496926208
id = 801100000000000000

for i in range(0, 1):
   # GET Search hashtag
   code, data = client.request("https://api.twitter.com/1.1/search/"
   + "tweets.json?q=%23HurricaneMatthew%0D%0Auntil%3A2016-12-01"
   + "&count=100"
   + "&result_type=recent"
   + "&since_id=" + str(id) )
   #+ "&until=2016-11-11" )
   #print code, '\n\n'
   #print data

   # Parse JSON data
   d = json.loads(data)
   for e in d['statuses']:
      if 'retweeted_status' in e: continue
      st = e['text']
      fWrite.write( e['created_at'].split()[1].encode('utf-8') + ',' + preprocess(st).encode('utf-8') + ',' + st.replace('\n', ' ').encode('utf-8') + '\n' )

   fWrite.flush()
   id = d['statuses'][-1]['id']
   print id
   print d['statuses'][-1]['created_at']
   time.sleep(6)

