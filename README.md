# TweetUsr - a possible future tool for Twitter user profiling

The script ```features.py``` contains the ```extract_features``` function which returns a list of features for a list of tweepy Status objects. The main program of the script is used to extract features from a local dataset of SLovene tweets. The extracts are, however, included in the repository (````X.pickle```,```Y1.pickle``` and ```Y2.pickle```).

The script ```learn.py``` uses the datasets serialized by ```features.py``, performs grid search, reports a classification report of the optimized classifier and trains and serializes an SVM classifier learned on all data.

The classification report is this:

```
             precision    recall  f1-score   support

  corporate       0.80      0.80      0.80      1460
    private       0.93      0.93      0.93      4382

avg / total       0.90      0.90      0.90      5842

```

The script ```predict.py``` is an exemplary classification process using the classifier serialized through ```learn.py```. The script takes a folder with a users' pickled tweepy Status objects and prints out the prediction. Rather fake examples (as they were learned on) are these:

```
$ python predict.py /home/nikola/tools/tweetpub/statuses/dfiser3/
['private']
$ python predict.py /home/nikola/tools/tweetpub/statuses/24UR/
['corporate']
```
