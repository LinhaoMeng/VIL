from .util import get_embedded_data
from .Data import Data
from .Model import Model
# from nptsne import TextureTsne
from sklearn.manifold import TSNE
import numpy as np
import time

class ALController:
    def __init__(self,dataname,initial_n,modelname) -> None:
        self.data = Data(dataname,initial_n)
        if(initial_n==0):
            self.model = Model(modelname,len(self.data.labelnames),None,None)
        else:
            self.model = Model(modelname,len(self.data.labelnames),self.data.X_raw[self.data.indices],self.data.y_raw[self.data.indices])
        self.dataembedding = TSNE(n_components=2, learning_rate='auto',init='random', perplexity=10).fit_transform(self.data.X_raw).reshape((self.data.X_raw.shape[0], 2))

    
    def updatedata(self, new_labelled_indices, new_labels):
        self.data.update_training_data(new_labelled_indices,new_labels)
        length = len(new_labelled_indices)
        for i in range(length):
            self.data.labelarr[new_labelled_indices[i]] = new_labels[i]

    def iter_train(self, new_labelled_indices, new_labels):
        X_new_labelled = self.data.X_raw[new_labelled_indices]
        self.model.teach(X_new_labelled,new_labels)
        # self.data.update_pool(new_labelled_indices)

    def get_predictions(self):
        return self.model.get_predict(self.data.X_raw)
    
    def get_predprobs(self):
        return self.model.get_predict_proba(self.data.X_raw)

    def get_prediction_probs(self):
        classes = self.model.learner.estimator.classes_.tolist()
        predicitons = self.model.get_predict(self.data.X_raw)
        probs = self.model.get_predict_proba(self.data.X_raw)
        return probs[np.arange(len(probs)), [classes.index(prediciton) for prediciton in predicitons]]

    def get_modelmetrics(self):
        return self.model.get_score(self.data.X_test,self.data.y_test)

    def get_candidates(self,strategy):
        self.model.update_strategy(strategy)
        indices = np.array([i for i in range(len(self.data.training_indices)) if self.data.training_indices[i] == 0])
        query_idx, _ = self.model.get_query(self.data.X_raw[indices])
        return indices[query_idx]

    def get_modelprob_projection(self):
        probs = self.model.get_predict_proba(self.data.X_raw)
        return get_embedded_data(probs)


 