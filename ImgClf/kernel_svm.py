#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, metrics
import time
from sklearn.multiclass import OneVsRestClassifier


gram = []
y = []
ids = []

for line in file("./kernel.dat"):
	terms = line.rstrip().split(",")
	ids.append(int(terms[0]))
	y.append(int(terms[1]))
	sim = []
	for i in terms[2:]:
		sim.append(i)
	gram.append(sim)


index = np.arange(0, len(ids))
np.random.shuffle(index)
index = list(index)
offset = int(len(index) * 0.7)


gram_train = []
y_train = []
for i in index[:offset]:
	tmp = []
	for j in index[:offset]:
		tmp.append(gram[i][j])
	gram_train.append(tmp)
	y_train.append(y[i])

gram_test = []
y_test = []
for i in index[offset:]:
	tmp = []
	for j in index[:offset]:
		tmp.append(gram[i][j])
	gram_test.append(tmp)
	y_test.append(y[i])

print offset
print len(gram_train)

#clf = OneVsRestClassifier(svm.SVC(kernel='precomputed'))
clf = svm.SVC(verbose=True, kernel='precomputed', max_iter=99999999)
print "fitting the model"
clf.fit(gram_train, y_train)

print "predicting"
y_predict = list(clf.predict(gram_test))

log = open('log.txt', "a")

print >> log, time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
print >> log, "Classification report for classifier %s:\n%s\n" % (clf, metrics.classification_report(y_test, y_predict))

print >> log, "Confusion matrix:\n%s" % metrics.confusion_matrix(y_test, y_predict)

log.close()

print y_predict
print y_test

count = 0
for i in range(len(y_predict)):
	if y_predict[i] == y_test[i]:
		count += 1

rate = count * 1.0/ len(y_predict)
print rate

