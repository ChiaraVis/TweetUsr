# TweetUsr - a possible future tool for Twitter user profiling

The script ```features.py``` contains the ```extract_features(statuses)``` function which returns a list of features for a list of tweepy Status objects.

The main program of the script is used to extract features from a local dataset of Slovene tweets. The lack of this dataset in the repo can be circumvented in three ways:
- one can use the feature extracts that are included in the repository (````X.pickle```,```Y1.pickle``` and ```Y2.pickle```, Y1 is a 5-class target, Y2 the used 2-class target)
- the file ```user_annotations``` contains Twitter user names and their annotations by both schemata (5-class, 2-class), one can use tweepy to download the timeline of those users
- one can go over to the prediction directly as the serialization of the classification model is included in the repo (see below)

The script ```learn.py``` uses the ```*.pickle``` datasets serialized by ```features.py```, performs grid search, gives a classification report of the optimized classifier (below) and trains and serializes an SVM classifier with optimized hyperparameters which is learned on all Slovene data.

```
             precision    recall  f1-score   support

  corporate       0.80      0.80      0.80      1460
    private       0.93      0.93      0.93      4382

avg / total       0.90      0.90      0.90      5842

```

The script ```predict.py``` is an example script of the classification process which uses the classifier serialized through ```learn.py```. The script takes a folder with pickled tweepy Status objects of a user and prints out the prediction together with class probabilities. Rather fake examples (as they were in part used for learning already) can be run on samples of status objects of two users:

```
$ python predict.py status_samples/dfiser3/
private [ 0.02420828  0.97579172]
$ python predict.py status_samples/24UR/
corporate [ 0.67101796  0.32898204]
```
