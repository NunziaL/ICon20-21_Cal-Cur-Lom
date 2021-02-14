#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

""" 
Viene effettuata la fase di preprocessing in cui il dataset viene diviso in training set e test set.
La colonna target è divisa dai restanti attributi perchè è la colonna su cui saranno effettuate le predizioni.
I valori di X sono standardizzati per ottenere valori confrontabili e pesati quando si effettuano i calcoli.
"""
def preprocess_inputs(df):
    df = df.copy()
    
    #Cancella le colonne delle categorie track, artist e uri
    df = df.drop(['track', 'artist', 'uri'], axis=1)
    
    #Split di df in X e y
    y = df['target']
    X = df.drop('target', axis=1)
    
    #Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, shuffle=True, random_state=1)
    
    #Standardizzazione dei valori di X
    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train = pd.DataFrame(scaler.transform(X_train), index=X_train.index, columns=X_train.columns)
    X_test = pd.DataFrame(scaler.transform(X_test), index=X_test.index, columns=X_test.columns)
    
    return X_train, X_test, y_train, y_test


""" 
Viene effettuata la fase di training dei modelli
"""
def train_model(name,model,X_train, X_test, y_train, y_test):
    
    model.fit(X_train, y_train)
    print(name + " trained.")
    
    print(name + ": {:.2f}%".format(model.score(X_test, y_test) * 100))

    #carica modello su file
    filename = name+'.sav'
    joblib.dump(model,filename)
    return model


"""
Viene predetto per ogni modella se la canzone inserita in input dall'utente è una hit oppure no.
Se la canzone è una hit la funzione  di predizione restituirà come output 1, altrimenti 0 in base alle loro probabilità.
"""
def previsione(data,song):
    X_train, X_test, y_train, y_test = preprocess_inputs(data)

    #Viene istanziato un dizionario con i seguenti modelli
    models = {
        "Logistic Regression": LogisticRegression(),
        "K-Nearest Neighbors": KNeighborsClassifier(),
        "Decision Tree": DecisionTreeClassifier(),
        "Neural Network": MLPClassifier(),
        "Random Forest": RandomForestClassifier(),
        "Gradient Boosting": GradientBoostingClassifier()
        }
    result=dict()
    
    #Viene effettuata la predizione per ogni modello attraverso la funzione predict()
    for name, model in models.items(): 
        #Si controlla se il file corrispondente al modello nel dizionario esiste al fine di allenarlo o no.
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