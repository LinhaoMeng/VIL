from modAL.models import ActiveLearner
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from modAL.uncertainty import uncertainty_sampling
from modAL.density import information_density

import time

class Model(object):
    def __init__(self,name,classnum,X_train,y_train):
        start = time.time()
        if name=="KNN":
            classifier = KNeighborsClassifier(n_neighbors=classnum)
        if name=='SVM':
            classifier = svm.SVC(probability=True)
        self.learner = ActiveLearner(estimator=classifier, query_strategy=uncertainty_sampling,X_training=X_train, y_training=y_train)
        print(f"Runtime of the initmodel is {time.time() - start}")

    def get_strategyname(self):
        return self.learner.query_strategy

    def teach(self,X,y):
        self.learner.teach(X=X,y=y)

    def get_predict(self,X):
        return self.learner.predict(X)

    def get_predict_proba(self,X):
        return self.learner.predict_proba(X)

    def get_score(self,X,y):
        return self.learner.score(X,y)

    def get_query(self,X_pool):
        return self.learner.query(X_pool)
    
    def update_strategy(self,strategy):
        if strategy == 'uncertainty':
            self.learner.query_strategy = uncertainty_sampling
        if strategy == 'density':
            self.learner.query_strategy = information_density