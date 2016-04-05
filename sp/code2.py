import sys
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
from sklearn.metrics import log_loss
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier


def sigmoid(y_pred):
    return 1 / (1 + np.exp(-y_pred))

data = pd.read_csv('gbm-data.csv', header=0)
data = np.array(data.values)
y = data[:, 0]
X = data[:, 1:]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.8, random_state=241)

learning_rate = [1, 0.5, 0.3, 0.2, 0.1]
learning_rate = [0.2]

for rate in learning_rate:
    log_loss_train = []
    log_loss_test = []

    clf = GradientBoostingClassifier(
        n_estimators=250, learning_rate=rate, verbose=False, random_state=241)
    predictions = clf.fit(X_train, y_train)

    for i, y_pred in enumerate(clf.staged_decision_function(X_train)):
        log_loss_train.append(log_loss(y_train, sigmoid(y_pred)))

    for i, y_pred in enumerate(clf.staged_decision_function(X_test)):
        log_loss_test.append(log_loss(y_test, sigmoid(y_pred)))

    log_loss_test = np.array(log_loss_test)

    # overfitting
    # print round(np.amin(log_loss_test), 2), np.argmin(log_loss_test)
    # 0.53 36

clf = RandomForestClassifier(n_estimators=36, random_state=241)
clf.fit(X_train, y_train)

predictions = clf.predict_proba(X_test)

score = log_loss(y_test, predictions)

print round(score, 2)

# 0.54
