#-*- coding: utf-8 -*-
from dataframe import *
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import SGDClassifier
from feat import description_dict, query_dict, keyword_dict, user_dict, title_dict



training_set_file = "data/sub_training.txt"
val_set_file = "data/validation.txt"

print "loading preprocess data"

description_word_weight = load_dict("data/description_tf_idf.txt", flag=False)
query_word_weight = load_dict("data/query_tf_idf.txt", flag=False)
keyword_word_weight = load_dict("data/keyword_tf_idf.txt", flag=False)
title_word_weight = load_dict("data/title_tf_idf.txt", flag=False)

ctr_ad = load_dict("data/ctr_ad.txt")
ctr_advertiser = load_dict("data/ctr_advertiser.txt")
ctr_user = load_dict("data/ctr_user.txt")
ctr_query = load_dict("data/ctr_query.txt")

CLICK, IMPR, DISPLAYURL, AD, ADVERTISER, DEPTH, POSITION, QUERY, KEYWORD, TITLE, DESCRIPTION, USER = range(12)

print "load training set"

def data_construct(filename):
	#数据加载
	X_sparse = []
	X_real = []
	Y = []

	for line in file(training_set_file):
		
		terms = line.rstrip().split("\t")

		ins_sparse = {}
		ins_sparse["AD."+terms[AD]] = 1
		#ins_sparse["ADVERTISER."+terms[ADVERTISER]] = 1
		ins_sparse["USER."+terms[USER]] = 1
		ins_sparse["QUERY."+terms[QUERY]] = 1
		ins_sparse["POSITIONDEPTH."+terms[POSITION]+"."+terms[DEPTH]] = 1

		if terms[USER] == '0':
			continue

		uid, gender, age = user_dict[terms[USER]].rstrip().split("\t")
		ins_sparse["GENDER."+gender] = 1
		ins_sparse["AGE."+age] = 1

		ins_real = []
		
		ins_real.append(float(ctr_ad[terms[AD]])) #pCTR_AD
		ins_real.append(float(ctr_advertiser[terms[ADVERTISER]])) #pCTR_ADVERTISER
		ins_real.append(float(ctr_user[terms[USER]]))
		ins_real.append(float(ctr_query[terms[QUERY]]))
		
		ins_real.append(float(terms[USER]))
		ins_real.append(float(terms[QUERY]))
		
		query = query_dict[terms[QUERY]]
		tokens = query.rstrip().split("|")
		ins_real.append(len(tokens))
		ins_sparse["QUERYTOKEN."+str(len(tokens))] = 1

		title = title_dict[terms[TITLE]]
		tokens = title.rstrip().split("|")
		ins_real.append(len(tokens))

		description = description_dict[terms[DESCRIPTION]]
		tokens = description.rstrip().split("|")
		ins_real.append(len(tokens))

		keyword = keyword_dict[terms[KEYWORD]]
		tokens = keyword.rstrip().split("|")
		ins_real.append(len(tokens))

		click = int(terms[0])
		impr = int(terms[1])

		for _ in range(impr):
			X_sparse.append(ins_sparse)
			X_real.append(ins_real)
		
		for _ in range(click):
			Y.append(1)
		for _ in range(impr-click):
			Y.append(-1)

	return X_sparse, X_real, Y

X_train_sparse, X_train_real, Y_train = data_construct(training_set_file)



print "model training"

dv = DictVectorizer(sparse=True)
X_train_sparse = dv.fit_transform(X_train_sparse)

clf = SGDClassifier(loss='log', penalty='l1')

N = len(Y_train)

for ix in range(N):
	X = X_train_sparse[ix].toarray().tolist()[0] + X_train_real[ix] 
	Y = [Y_train[ix]]
	clf.partial_fit(X, Y, classes=[-1,1])

#模型保存
from sklearn.externals import joblib
joblib.dump(clf, './lr/model.pkl')



print "model evaluation"

X_val_sparse, X_val_real, y_val = data_construct(val_set_file)
		
N = len(y_val)

X_val_sparse = dv.transform(X_val_sparse)
y_predict = []
for ix in range(N):
	X = X_val_sparse[ix].toarray().tolist()[0] + X_val_real[ix]
	y = clf.predict_proba(X)
	y_predict.append( y.tolist()[0])

import numpy as np
y_predict = np.array(y_predict)

#评估
from sklearn.metrics import classification_report, roc_curve, auc

fpr, tpr, thresholds = roc_curve(y_val, y_predict[:, 1])

roc_auc = auc(fpr, tpr)

print "auc: ", str(roc_auc)

fd =open("./lr/log.txt", "a")

#记录实验时间
from datetime import datetime
dt = datetime.now()

print >> fd, dt.strftime('%y-%m-%d %H:%M:%S')
print >> fd, "auc:", str(roc_auc)
print >> fd, "fpr:", ",".join(map(str, fpr.tolist()))
print >> fd, "tpr:", ",".join(map(str, tpr.tolist()))
print >> fd, "thresholds:", ",".join(map(str, thresholds.tolist()))
print >> fd, ""
print >> fd, ""

fd.close()

figure(1)
plot(fpr, tpr, label='ROC curve')
plot([0, 1], [0, 1], 'k--')
xlim([0.0, 1.0])
ylim([-0.05, 1.05])
xlabel('False Positive Rate')
ylabel('True Positive Rate')

show()




