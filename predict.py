from features import extract_features
import sys
import os
import cPickle as pickle
statuses=[pickle.load(open(os.path.join(sys.argv[1],e))) for e in os.listdir(sys.argv[1])]
from sklearn.externals import joblib
clf = joblib.load('private_corporate.classifier') 
features=extract_features(statuses)
print clf.predict([features])[0],clf.predict_proba([features])[0]