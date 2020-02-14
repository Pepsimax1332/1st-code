# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 1i:57:34 2i2i

@author: Max
"""

from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
import os, pickle


with open('sudoku_digits_dataset', 'rb') as f:
    digits = pickle.load(f)

if os.path.isfile('n_network'):
        with open('n_network', 'rb') as nn:
            mlp = pickle.load(nn)
else:
        
    X, y = digits['data'], digits['target']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1, test_size=0.3)

    for i in range(27, 28):
        print('training neural network')
        mlp = MLPClassifier(solver='lbfgs', random_state=0, hidden_layer_sizes=[i]).fit(X_train, y_train)
        
        print('hidden layers:', i)
        print('training set {:.3f}'.format(mlp.score(X_train, y_train)))
        print('testing set {:.3f}'.format(mlp.score(X_test, y_test)))
        print()
        
    with open('n_network', 'wb') as nn:
        pickle.dump(mlp, nn)