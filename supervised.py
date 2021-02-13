# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 21:34:04 2021

@author: lomon
"""
import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC, SVC
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

def preprocess_inputs(df):
    df = df.copy()
    
    # Drop high-cardinality categorical columns
    df = df.drop(['track', 'artist', 'uri'], axis=1)
    
    # Split df into X and y
    y = df['target']
    X = df.drop('target', axis=1)
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, shuffle=True, random_state=1)
    
    # Scale X
    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train = pd.DataFrame(scaler.transform(X_train), index=X_train.index, columns=X_train.columns)
    X_test = pd.DataFrame(scaler.transform(X_test), index=X_test.index, columns=X_test.columns)
    
    return X_train, X_test, y_train, y_test

def train_model(name,model,X_train, X_test, y_train, y_test):
    
    model.fit(X_train, y_train)
    print(name + " trained.")
        
    print(name + ": {:.2f}%".format(model.score(X_test, y_test) * 100))

    """caricare modello su file"""
    filename = name+'.sav'
    joblib.dump(model,filename)
    return model

def previsione(data,song):
    X_train, X_test, y_train, y_test = preprocess_inputs(data)

    models = {
        "Logistic Regression": LogisticRegression(),
        "K-Nearest Neighbors": KNeighborsClassifier(),
        "Decision Tree": DecisionTreeClassifier(),
        "Neural Network": MLPClassifier(),
        "Random Forest": RandomForestClassifier(),
        "Gradient Boosting": GradientBoostingClassifier()
        }
    result=dict()
    for name, model in models.items(): 
        filename = 'data/' + name + '.sav'
        if(os.path.exists(filename)):
            model = joblib.load('data/' + name +'.sav')
            result[name] = model.predict(song)[0]
            print(name + " " + str(result[name]))
        else:
            model = train_model(name,model,X_train, X_test, y_train, y_test)
            result[name] = model.predict(song)[0]
            print(name + " " + str(result[name]))
    return result