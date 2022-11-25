import pickle
# from nptsne import TextureTsne
from sklearn.manifold import TSNE
import os
import time

# access data and return data as X-array, y-label array, labelnames
def get_data(name):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    print(SITE_ROOT)
    if name == 'MNIST':
        with open(SITE_ROOT+'/mnist_train.pickle', 'rb') as handle:
            train_data = pickle.load(handle) 
        datatype = 'image'
        ids = train_data['ids']
        X = train_data['data']/255.0
        y = train_data['target']
        labelnames = train_data['target_names']
        with open(SITE_ROOT+'/mnist_test.pickle', 'rb') as handle:
            test_data = pickle.load(handle)
        test_X = test_data['data']/255.0
        test_y = test_data['target']
    return ids,X,y,labelnames,datatype,test_X,test_y

def get_embedded_data(X):
    start = time.time()
    rowcount = X.shape[0]
    X_embedded = TSNE(n_components=2, learning_rate='auto',init='random', perplexity=10).fit_transform(X)
    X_embedded = X_embedded.reshape((rowcount, 2))
    print(f"Runtime of the get_embedded_data is {time.time() - start}")
    return X_embedded

