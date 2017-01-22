#!/usr/bin/python

import cPickle as pickle
import numpy as np
import sys

X=np.asarray(pickle.load(open('../1-slovene/X.pickle')))
Y1=np.asarray(pickle.load(open('../1-slovene/Y1.pickle')))
Y2=np.asarray(pickle.load(open('../1-slovene/Y2.pickle')))
x_names=['mean_len_text','median_len_text','variance_len_text','percentage_http','percentage_mention','percentage_hash','percentage_question','percentage_ellipsis','percentage_comma','percentage_exclamation','percentage_emoji','percentage_inreply','mean_retweet_count','median_retweet_count','variance_retweet_count','percentage_retweeted','mean_favorite_count','median_favorite_count','variance_favorite_count','percentage_favorited','percentage_is_quote','mean_hour','median_hour','variance_hour','mean_day','median_day','variance_day','percentage_working_hours','percentage_weekend','percentage_web_client','percentage_truncated','user_statuses_count','user_statuses_per_day','user_followers_count','user_friends_count','user_followers_friends_ratio','user_listed_count','user_favourites_count']

import sklearn
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score,f1_score,confusion_matrix,classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import cross_val_predict

from sklearn.dummy import DummyClassifier
dclf=DummyClassifier(strategy='most_frequent')

parms={'clf__C': [2**x for x in range(-5,16,2)], 'clf__gamma': [2**x for x in range(-15,4,2)], 'clf__kernel': ['rbf']}
clf=Pipeline([('scaler',StandardScaler()),('clf',SVC())])

print 'performing grid search'
grid_search=GridSearchCV(clf,parms,n_jobs=23,verbose=0,scoring='f1_weighted')
grid_search.fit(X,Y2)
print 'grid search best score',grid_search.best_score_

clf_best=grid_search.best_estimator_
Y2_pred=cross_val_predict(clf_best,X,Y2)
print classification_report(Y2,Y2_pred)

clf_best.fit(X,Y2)
from sklearn.externals import joblib
joblib.dump(clf_best, 'private_corporate.classifier')
