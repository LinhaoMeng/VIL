from .util import get_data, get_embedded_data
import numpy as np
import time

class Data(object):
    # initial_n samples are used as initial labelled data for model training
    def __init__(self,name,initial_n):
        self.name=name
        self.ids, self.X_raw, self.y_raw, self.labelnames, self.datatype, self.X_test, self.y_test = get_data(name)
        n_X_raw = self.X_raw.shape[0]
        self.arrlen = n_X_raw
        # labelarr records all manual labels 
        self.labelarr = np.full(n_X_raw,-1) 
        self.indices = np.random.randint(low=0, high=n_X_raw, size=int(initial_n*n_X_raw))
        self.training_indices = np.zeros(n_X_raw)
        self.training_indices[self.indices]=1
        for i in self.indices:
            self.labelarr[i] = self.y_raw[i]
        # self.embedding = get_embedded_data(self.X_raw)

    def query_ids(self,indices):
        return self.ids[indices]

    def query_labels(self,indices):
        return self.y_raw[indices]

    def get_embedding(self):
        return self.embedding

    def update_pool(self,query_idx):
        self.X_pool = np.delete(self.X_pool, query_idx, axis=0)
        self.y_pool = np.delete(self.y_pool, query_idx, axis=0)

    def update_training_data(self,newindices,new_labels):
        for index,label in zip(newindices,new_labels):
            self.labelarr[index]=label
            self.training_indices[index]=1

    def query_datapath(self,indices,labels,ids):
        length = len(ids)
        paths = []
        for i in range(length):
            paths.append({
                'index':indices[i],
                'path':'/'+self.name+'/training/'+ self.labelnames[labels[i]]+'/'+ids[i]+'.png'})
        return paths
