from sklearn import datasets, svm
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import pip

#pip.main(["install", "scipy"])

iris = datasets.load_iris()
digits = datasets.load_digits()
"""
print(len(digits.data))
clf = svm.SVC()
clf.fit(digits.data[0:1700], digits.target[0:1700])
predict = clf.predict(digits.data[1700:1797])
target = digits.target[1700:1797]
"""

X = np.array([[1,2],[5,8],[1.5,1.8],[8,8],[1,.6],[9,11]])
y = np.array([0,1,0,1,0,1])
clf = svm.SVC(kernel='linear', C=1.0)
clf.fit(X,y)
print(clf.predict([[.58,.76],[10,10]]))
