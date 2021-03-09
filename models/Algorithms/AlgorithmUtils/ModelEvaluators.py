from datetime import date
import pandas as pd
import numpy as np
import random
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import sklearn.metrics as metrics
from sklearn.cluster import KMeans

def remove_useless_params(model, X, y, threshold):

    features = list(X.columns)
    bad_features = {}

    
    for i in range(5):
        
        iter_X = X.copy()
        bestPrecision = cv_model_precision(model, X, y, threshold)
        
        print("-------------------------")
        print("Iteration {}".format(i + 1))
        random.shuffle(features)
        
        for feature in features:
            tempX = iter_X.drop(columns = feature)
            precision = cv_model_precision(model, tempX, y, threshold)
            if precision > bestPrecision:
                bestPrecision = precision
                iter_X = tempX
                print("{} is not useful".format(feature))
                print(bestPrecision)
                if feature not in bad_features:
                    bad_features[feature] = 1
                else:
                    bad_features[feature] += 1
    
    return bad_features
