from sklearn import datasets, svm
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import random
import time
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
start = time.time()
X = list()
y = list()  # try using 0s and 1s instead
f = open('Movie Dataset for Machine Learning.txt', 'r')
count = 0
for line in f:
    if count != 0:
        line = line.strip('\n').split('\t')
        data_point = [float(line[0]), float(line[1])]
        X.append(data_point)
        y.append(int(line[2]))
    count += 1

for i in range(5):
    c = list(zip(X,y))
    random.shuffle(c)
    X, y = zip(*c)
    clf = svm.SVC()
    clf.fit(X[0:2000],y[0:2000])
    predictions = clf.predict(X[2000:2677])
    print(accuracy_score(y[2000:2677], predictions))
    done = time.time()

"""
X = np.array([[1,2],[5,8],[1.5,1.8],[8,8],[1,.6],[9,11]])
y = np.array([0,1,0,1,0,1])
clf = svm.SVC(kernel='linear', C=1.0)
clf.fit(X,y)
print(clf.predict([[.58,.76],[10,10]]))
"""
