import numpy as np
from statistics import mode

class KNearestNeighbors:
    
    def __init__(self, k):
        self.k = k
    
    def fit(self, x_train, y_train):
        self.x = x_train
        self.y = y_train
        
    def euclidean_distance(self, x1, x2):
        return np.sqrt(np.sum((x1-x2)**2))
        
    def predict(self, x):
        distances=[]
        for p in self.x:
            distances.append(self.euclidean_distance(x, p))
        nearest = np.argsort(distances)
        Knearest = nearest[ :self.k]
        Knearest_labels = [self.y[i] for i in Knearest]
        return mode(Knearest_labels)
        
    def evaluate(self, x, y):
        corrects = 0
        for i in range(len(x)):
            if self.predict(x[i]) == y[i]:
                corrects+=1
        return corrects/len(x)