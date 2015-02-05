from sklearn import svm
from sklearn.datasets import make_multilabel_classification

X = [[1, 0], [1, 1], [0, 1]]
y = [1, 2, 3]

clf = svm.SVC()
clf.fit(X, y)
