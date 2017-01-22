#!/usr/bin/python
#-*-coding:utf8-*-
import cPickle as pickle
import numpy as np
import re
from datetime import datetime
import os
import sys

def mean_median_variance(statuses,function):
  measurements=[]
  for status in statuses:
    measurements.append(function(status))
  return np.mean(measurements),np.median(measurements),np.var(measurements)

def percentage(statuses,function):
  count=0.
  for status in statuses:
    if function(status):
      count+=1
  return count/len(statuses)

def user_meta(statuses,function):
  return function(statuses)

emoji_pattern=re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "]",re.UNICODE)

def extract_features(statuses):
  x=[]
  ### tweet text features ###
  # mmv of tweet length
  x.extend(mean_median_variance(statuses,lambda x:len(x.text)))
  # URL
  x.append(percentage(statuses,lambda x:'http' in x.text))
  # mention
  x.append(percentage(statuses,lambda x:'@' in x.text))
  # hash
  x.append(percentage(statuses,lambda x:'#' in x.text))
  # question mark
  x.append(percentage(statuses,lambda x:'?' in x.text))
  # ellipsis
  x.append(percentage(statuses,lambda x:'...' in x.text or u'…' in x.text))
  # comma
  x.append(percentage(statuses,lambda x:',' in x.text))
  # exclamation mark
  x.append(percentage(statuses,lambda x:'!' in x.text))
  # emoji
  x.append(percentage(statuses,lambda x:emoji_pattern.search(x.text)!=None))
  ### tweet meta features ###
  # replies
  x.append(percentage(statuses,lambda x:x.in_reply_to_user_id!=None))
  # retweet count
  x.extend(mean_median_variance(statuses,lambda x:x.retweet_count))
  # retweeted
  x.append(percentage(statuses,lambda x:x.retweet_count>0))
  # favorite count
  x.extend(mean_median_variance(statuses,lambda x:x.favorite_count))
  # favorited
  x.append(percentage(statuses,lambda x:x.favorite_count>0))
  # quote
  x.append(percentage(statuses,lambda x:x.is_quote_status==True))
  # mmv of hour
  x.extend(mean_median_variance(statuses,lambda x:x.created_at.hour))
  # mmv of day
  x.extend(mean_median_variance(statuses,lambda x:x.created_at.weekday()))
  # during working hours
  x.append(percentage(statuses,lambda x:x.created_at.weekday()<6 and x.created_at.hour>=7 and x.created_at.hour<=18))
  # on weekend
  x.append(percentage(statuses,lambda x:x.created_at.weekday()>5))
  # source twitter web client
  x.append(percentage(statuses,lambda x:x.source==u'Twitter Web Client'))
  # truncated
  x.append(percentage(statuses,lambda x:x.truncated==True))
  ### user meta features ###
  # number of tweets
  x.append(user_meta(statuses,lambda x:x[-1].user.statuses_count))
  # number of tweets per day
  x.append(user_meta(statuses,lambda x:float(x[-1].user.statuses_count)/(datetime.now()-x[-1].user.created_at).days))
  # followers count
  x.append(user_meta(statuses,lambda x:x[-1].user.followers_count))
  # friends count
  x.append(user_meta(statuses,lambda x:x[-1].user.friends_count))
  # followers friends ratio
  x.append(user_meta(statuses,lambda x:float(x[-1].user.followers_count+0.1)/(x[-1].user.friends_count+0.1)))
  # listed_count
  x.append(user_meta(statuses,lambda x:x[-1].user.listed_count))
  # favourites_count
  x.append(user_meta(statuses,lambda x:x[-1].user.favourites_count))
  return x

if __name__=='__main__':
  y1=dict([(a,b) for a,b,c in [e[:-1].split('\t') for e in open('user_annotations')]])
  y2=dict([(a,c) for a,b,c in [e[:-1].split('\t') for e in open('user_annotations')]])

  X=[]
  x_names=['mean_len_text','median_len_text','variance_len_text','percentage_http','percentage_mention','percentage_hash','percentage_question','percentage_ellipsis','percentage_comma','percentage_exclamation','percentage_emoji','percentage_inreply','mean_retweet_count','median_retweet_count','variance_retweet_count','percentage_retweeted','mean_favorite_count','median_favorite_count','variance_favorite_count','percentage_favorited','percentage_is_quote','mean_hour','median_hour','variance_hour','mean_day','median_day','variance_day','percentage_working_hours','percentage_weekend','percentage_web_client','percentage_truncated','user_statuses_count','user_statuses_per_day','user_followers_count','user_friends_count','user_followers_friends_ratio','user_listed_count','user_favourites_count']
  Y1=[]
  Y2=[]
  X_text=[]

  balance=False
  count=0
  num_statuses=[]
  users=os.listdir('/home/nikola/tools/tweetpub/statuses/')
  for user_num,user in enumerate(users):
    if user not in y1:
      print 'unknown user',user
      continue
    statuses=[]
    files=os.listdir('/home/nikola/tools/tweetpub/statuses/'+user)
    # we take into account only users with 100 or more tweets
    if len(files)<100:
      continue
    count+=1
    print count,user,
    for file in files:
      statuses.append(pickle.load(open('/home/nikola/tools/tweetpub/statuses/'+user+'/'+file)))
    num_statuses.append(len(statuses))
    print 'loaded',
    ### text for bow ###
    X_text.append(' '.join([e.text for e in statuses]))
    X.append(extract_features(statuses))
    Y1.append(y1[user])
    Y2.append(y2[user])
    print 'extracted',
    print Y1[-1],Y2[-1],user,user_num+1,'/',len(users)
    sys.stdout.flush()

  pickle.dump(X,open('X.pickle','w'),1)
  pickle.dump(Y1,open('Y1.pickle','w'),1)
  pickle.dump(Y2,open('Y2.pickle','w'),1)
  pickle.dump(X_text,open('X_text.pickle','w'),1)
  print np.mean(num_statuses),np.median(num_statuses)
