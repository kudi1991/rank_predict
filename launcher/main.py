# -*- coding: utf-8 -*-
"""
Created on 2017/10/25 18:31

@author: zhangle
"""
import time
from sklearn import metrics


# Multinomial Naive Bayes Classifier
# 朴素贝叶斯分类器
def naive_bayes_classifier(train_x, train_y, weights=None):
    from sklearn.naive_bayes import GaussianNB
    model = GaussianNB()
    model.fit(train_x, train_y, weights)
    return model


# KNN Classifier
# 最邻近规则分类
def knn_classifier(train_x, train_y, weights=None):
    from sklearn.neighbors import KNeighborsClassifier
    model = KNeighborsClassifier()
    model.fit(train_x, train_y)
    return model


# Logistic Regression Classifier
# 逻辑回归分类器
def logistic_regression_classifier(train_x, train_y, weights=None):
    from sklearn.linear_model import LogisticRegression
    model = LogisticRegression(penalty='l2')
    model.fit(train_x, train_y, weights)
    return model


# Random Forest Classifier
# 随机森林分类器
def random_forest_classifier(train_x, train_y, weights=None):
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier(n_estimators=8)
    model.fit(train_x, train_y, weights)
    return model


# Decision Tree Classifier
# 决策树分类器
def decision_tree_classifier(train_x, train_y, weights=None):
    from sklearn import tree
    model = tree.DecisionTreeClassifier()
    model.fit(train_x, train_y, weights)
    return model


# GBDT(Gradient Boosting Decision Tree) Classifier
# 迭代决策树分类器
def gradient_boosting_classifier(train_x, train_y, weights=None):
    from sklearn.ensemble import GradientBoostingClassifier
    model = GradientBoostingClassifier(n_estimators=200)
    model.fit(train_x, train_y, weights)
    return model


# SVM Classifier
# 支持向量机分类器
def svm_classifier(train_x, train_y, weights=None):
    from sklearn.svm import SVC
    model = SVC(kernel='rbf', probability=True)
    model.fit(train_x, train_y, weights)
    return model


# SVM Classifier using cross validation
# 交叉验证 支持向量机分类器
def svm_cross_validation(train_x, train_y, weights=None):
    from sklearn.model_selection import GridSearchCV
    from sklearn.svm import SVC
    model = SVC(kernel='rbf', probability=True)
    param_grid = {'C': [1e-3, 1e-2, 1e-1, 1, 10, 100, 1000], 'gamma': [0.001, 0.0001]}
    grid_search = GridSearchCV(model, param_grid, n_jobs=1, verbose=1)
    grid_search.fit(train_x, train_y)
    best_parameters = grid_search.best_estimator_.get_params()
    # for para, val in list(best_parameters.items()):
    #     print(para, val)
    model = SVC(kernel='rbf', C=best_parameters['C'], gamma=best_parameters['gamma'], probability=True)
    model.fit(train_x, train_y, weights)
    return model

if __name__ == '__main__':
    from sklearn import model_selection
    from sklearn import preprocessing
    import numpy as np
    from data.data_process import read_data

    data, target, weights = read_data()
    data = np.array(data)
    data = preprocessing.scale(data)
    train_x, test_x, train_y, test_y = model_selection.train_test_split(data, target, test_size=0.2, random_state=0)
    classifiers = {'NB': naive_bayes_classifier,
                   'KNN': knn_classifier,
                   'LR': logistic_regression_classifier,
                   'RF': random_forest_classifier,
                   'DT': decision_tree_classifier,
                   'SVM': svm_classifier,
                   'GBDT': gradient_boosting_classifier,
                   # 'SVMCV': svm_cross_validation,
                   }

    print('reading training and testing data...')

    for name, classifier in classifiers.items():
        print('******************* %s ********************' % classifier)
        start_time = time.time()
        model = classifier(train_x, train_y)
        print('training took %fs!' % (time.time() - start_time))
        predict = model.predict(test_x)
        precision = metrics.precision_score(test_y, predict, average='micro')
        recall = metrics.recall_score(test_y, predict, average='micro')
        print('precision: %.2f%%, recall: %.2f%%' % (100 * precision, 100 * recall))
        accuracy = metrics.accuracy_score(test_y, predict)
        print('accuracy: %.2f%%' % (100 * accuracy))
