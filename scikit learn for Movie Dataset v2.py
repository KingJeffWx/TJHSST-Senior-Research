from sklearn import datasets, svm
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import math
import statistics
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
        #budget = math.log(float(line[0]), 10)
        budget = (math.log(float(line[0]), 10) - 7.34170275069) / 0.6041856642537966    # normalized
        #rating = float(line[1])*2
        rating = (float(line[1])*2 - 6.25481388255) / 1.0229395099729501    # normalized
        month = int(line[2])
        data_point = [budget, rating, month]
        X.append(data_point)
        y.append(int(line[3]))
    count += 1

### SVM and others ######

iterations = 1
avg_score = 0.0
for i in range(iterations):
    c = list(zip(X,y))
    random.shuffle(c)
    X, y = zip(*c)
    clf = svm.SVC(kernel='rbf')
    #clf = svm.SVC(kernel='linear', C=1)
    #clf = GaussianProcessClassifier()
    #clf = DecisionTreeClassifier()
    #clf = RandomForestClassifier(n_estimators=50)
    #clf = GaussianNB()
    #clf = AdaBoostClassifier()
    #clf = QuadraticDiscriminantAnalysis()
    clf.fit(X[0:2100],y[0:2100])
    predictions = clf.predict(X[2100:2677])
    avg_score += accuracy_score(y[2100:2677], predictions)
    print(accuracy_score(y[2100:2677], predictions))
avg_score /= iterations
#print(avg_score)


"""
#### KNN #######
knn_size = 1
while knn_size < 1000:
    iterations = 10
    avg_score = 0.0
    for i in range(iterations):
        c = list(zip(X,y))
        random.shuffle(c)
        X, y = zip(*c)
        #clf = svm.SVC(kernel='rbf')
        clf = KNeighborsClassifier(knn_size)
        clf.fit(X[0:2100],y[0:2100])
        predictions = clf.predict(X[2100:2677])
        avg_score += accuracy_score(y[2100:2677], predictions)
    avg_score /= iterations
    print(knn_size, avg_score)
    knn_size += 1
"""




#### Section for plotting points below ####

budgets = list()
ratings = list()
colors = list()
for i in range(len(X)):
    budgets.append(X[i][0])
    ratings.append(X[i][1])
    if y[i] == 1:
        colors.append('g')
    else:
        colors.append('r')
plt.scatter(budgets, ratings, s=3, c=colors)
plt.xlim(-5,5)
plt.ylim(-5,5)
plt.show()


done = time.time()
print("Time taken:", str(done - start))
"""
X = np.array([[1,2],[5,8],[1.5,1.8],[8,8],[1,.6],[9,11]])
y = np.array([0,1,0,1,0,1])
clf = svm.SVC(kernel='linear', C=1.0)
clf.fit(X,y)
print(clf.predict([[.58,.76],[10,10]]))
"""
