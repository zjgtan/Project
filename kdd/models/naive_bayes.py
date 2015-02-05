#-*- coding: utf-8 -*-
from pylab import *
from sklearn.feature_extraction import DictVectorizer
from sklearn.naive_bayes import BernoulliNB
import math

training_set_name = "sub_training.txt"
val_set_name = "validation.txt"

def load_tab_dict(filename):
	d = {}
	for line in file(filename):
		key, value = line.rstrip().split("\t")
		d[key] = value
	return d

titleid = load_tab_dict("../track2/titleid_tokensid.txt")
queryid = load_tab_dict("../track2/queryid_tokensid.txt")

"""
AdIDs = set()
positions = set()
UserIDs = set()
"""
QueryID = set()
TitleID = set()

title_query_sim = {}

for line in file(training_set_name):
	terms = line.rstrip().split("\t")
	"""
	AdIDs.add(terms[3])
	positions.add(terms[6])
	UserIDs.add(terms[11])
	"""
	QueryID.add(terms[7])
	TitleID.add(terms[9])
	title_query_sim[terms[9]+','+terms[7]] = 0

"""
AdIDs = dict([(ID, ix) for ix, ID in enumerate(AdIDs)])
positions = dict([(ID, ix) for ix, ID in enumerate(positions)])
UserIDs = dict([(ID, ix) for ix, ID in enumerate(UserIDs)])
"""
QueryID = dict([(ID, ix) for ix, ID in enumerate(QueryID)])
TitleID= dict([(ID, ix) for ix, ID in enumerate(TitleID)])

#tf-idf
words_doc_freq = {}
def doc_frequency(docs, dict):
	for ID in docs:
		doc = dict[ID].rstrip().split("|")
		for word in doc:
			words_doc_freq.setdefault(word, 0)
			words_doc_freq[word] += 1

doc_frequency(QueryID, queryid)
doc_frequency(TitleID, titleid)

Ndoc = len(QueryID) + len(TitleID)

del QueryID
del TitleID

#计算query和title的cos相似度
def tf_idf(doc):
	word_freq = {}
	for word in doc:
		word_freq.setdefault(word, 0)
		word_freq[word] += 1

	tfidf = {}
	for word in word_freq:
		tfidf[word] = word_freq[word] * 1.0  / max(word_freq.values()) * math.log(Ndoc * 1.0 / (words_doc_freq[word] + 1))
	return tfidf

def sparse_cos_sim(vector1, vector2):
	return sum([vector1[key] * vector2[key] for key in vector1 if key in vector2]) / math.sqrt(sum([w ** 2 for w in vector1.values()])) / math.sqrt(sum([w ** 2 for w in vector2.values()]))

#计算所有可能的相似度
for key in title_query_sim:
	tID, qID = key.split(",")
	title = titleid[tID].split("|")
	query = queryid[qID].split("|")
	title = tf_idf(title)
	query = tf_idf(query)
	title_query_sim[key] = sparse_cos_sim(title, query)

#相似度值离散化
sim_max = max(title_query_sim.values())
sim_min = min(title_query_sim.values())
interval = (sim_max - sim_min) / 10.0

#二值化
def binarize(id, dict):
	vector = [0] * len(dict)
	idx = dict[id]
	vector[idx] = 1
	return vector


#构造训练集

def load_data_set(filename):
	X = []
	y = []
	for line in file(training_set_name):
		feat = {}
		terms = line.rstrip().split("\t")
		#AdID
		"""
		vector = binarize(terms[3], AdIDs)
		feat += ",".join(map(str, vector))
		"""
		feat["AdID,"+terms[3]] = 1

		#position
		"""
		vector = binarize(terms[6], positions)
		feat += "," + ",".join(map(str, vector))
		"""
		feat["position,"+terms[6]] = 1

		#UserID
		"""
		vector = binarize(terms[11], UserIDs)
		feat += "," + ",".join(map(str, vector))
		"""
		feat["UserID,"+terms[11]] = 1

		#QueryID
		"""
		vector = binarize(terms[7], QueryID)
		feat += "," + ",".join(map(str, vector))
		"""
		feat["QueryID,"+terms[7]] = 1

		#tf-idf	
		idx = int((title_query_sim[terms[9]+","+terms[7]] - sim_min) / interval)
		if idx == 10: idx = 9
		"""
		vector = [0] * 10
		vector[idx] = 1
		feat += "," + ",".join(map(str, vector))
		"""
		feat["sim,"+str(idx)] = 1

		click, impr = int(terms[0]), int(terms[1])
		for _ in range(click):
			X.append(feat)
			y.append(1)

		for _ in range(impr - click):
			X.append(feat)
			y.append(-1)

	return X, y

X_train, y_train = load_data_set(training_set_name)

dv = DictVectorizer(sparse=True)
#确定列名，之后只要使用transform即可
X_train = dv.fit_transform(X_train)

clf = BernoulliNB()

clf.fit(X_train, y_train)

#模型保存
from sklearn.externals import joblib
joblib.dump(clf, 'model.pkl')

#释放内存空间
del X_train
del y_train


#加载测试数据
X_val, y_val = load_data_set(val_set_name)
X_val = dv.transform(X_val)
#预测
y_predict_prob = clf.predict_proba(X_val)
y_predict = clf.predict(X_val)


#评估
from sklearn.metrics import classification_report, roc_curve, auc
print classification_report(y_val, y_predict)

fpr, tpr, thresholds = roc_curve(y_val, y_predict_prob[:, 1])

roc_auc = auc(fpr, tpr)

print "auc: ", str(roc_auc)

fd =open("log.txt", "a")

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














