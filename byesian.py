#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 15:32:41 2021

@author: antoniocurci
"""

import pandas as pd
import joblib
import os
from math import sqrt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC, SVC
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier


import warnings
warnings.filterwarnings(action='ignore')

"Espressione regolare che cicla sui file della cartella con tutte le canzoni"
dfs = [pd.read_csv(f'archive/dataset-of-{decade}0s.csv') for decade in ['6', '7', '8', '9', '0', '1']]


for i, decade in enumerate([1960, 1970, 1980, 1990, 2000, 2010]):
    dfs[i]['decade'] = pd.Series(decade, index=dfs[i].index)

data = pd.concat(dfs, axis=0).sample(frac=1.0, random_state=1).reset_index(drop=True)

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

X_train, X_test, y_train, y_test = preprocess_inputs(data)

models = {
    "                   Logistic Regression": LogisticRegression(),
    "                   K-Nearest Neighbors": KNeighborsClassifier(),
    "                         Decision Tree": DecisionTreeClassifier(),
    "Support Vector Machine (Linear Kernel)": LinearSVC(), 
    "   Support Vector Machine (RBF Kernel)": SVC(),
    "                        Neural Network": MLPClassifier(),
    "                         Random Forest": RandomForestClassifier(),
    "                     Gradient Boosting": GradientBoostingClassifier()
}

def train_model(models,X_train, X_test, y_train, y_test):
    
    for name, model in models.items():
        model.fit(X_train, y_train)
        print(name + " trained.")
        
    for name, model in models.items():
        print(name + ": {:.2f}%".format(model.score(X_test, y_test) * 100))

    """caricare modello su file"""
    for name, model in models.items():
        filename = name+'.sav'
        joblib.dump(model,filename)
    return models
        
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

cid = 'c1f44332d14943bd9766a095aab44a37'
secret = '7b12a556717a4b17bbfcc7f19f4bf3d9'

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

"""prende in input il titolo della canzone"""
title = input("Dammi il titolo della canzone:")

"""trova la canzone dal titolo. limit è il numero di risultati"""
song = sp.search(title, limit=1, type="track")

"""prende l'uri della canzone"""
uriSong = song['tracks']['items'][0]['uri']
"""prende l'url http della canzone"""
urlSong = song['tracks']['items'][0]['external_urls']['spotify']

"""prendere le features della canzone"""
feature = sp.audio_features(uriSong)[0]
analysis= sp.audio_analysis(uriSong)

lst = {'danceability':[feature['danceability']],
       'energy':[feature['energy']],
       'key':[feature['key']],
       'loudness':[feature['loudness']],
       'mode':[feature['mode']],
       'speechiness':[feature['speechiness']],
       'acousticness':[feature['acousticness']],
       'instrumentalness':[feature['instrumentalness']],
       'liveness':[feature['liveness']],
       'valence':[feature['valence']],
       'tempo':[feature['tempo']],
       'duration_ms':[feature['duration_ms']],
       'time_signature':[feature['time_signature']],
       'chorus_hit':[ analysis["sections"][2]['start']],
       'sections':[len(analysis["sections"])], 
       'decade':[2000]}
X = pd.DataFrame(lst)

filename ="                   Logistic Regression"+'.sav'
if(os.path.exists(filename)):
    for name, model in models.items():
        model = joblib.load(name+'.sav')
        result = model.predict(X)
        print(name + " " + str(result[0]))
else:
    models = train_model(models,X_train, X_test, y_train, y_test)
    for name, model in models.items():
        result = model.predict(X)
        print(name + " " + str(result[0]))
        
#Classificatore Bayesiano
def separate_by_class(dataset):
	separated = dict()
	for i in range(len(dataset)):
		vector = dataset.iloc[i]
		class_value = vector['target']
		if (class_value not in separated):
			separated[class_value] = list()
		separated[class_value].append(vector)
	return separated
 
# Test separating data by class
separated = separate_by_class(data)

# Calculate the mean of a list of numbers
def mean(numbers):
	return sum(numbers)/float(len(numbers))

# Calculate the standard deviation of a list of numbers
def stdev(numbers):
	avg = mean(numbers)
	variance = sum([(x-avg)**2 for x in numbers]) / float(len(numbers)-1)
	return sqrt(variance)

# Calculate the mean, stdev and count for each column in a dataset
def summarize_dataset(dataset):
	"""trovare un modo per iterare sulle colonne di dataset"""
    summaries=[(mean(dataset['danceability']), stdev(dataset['danceability']), len(dataset['danceability']))]
    summaries.append([(mean(dataset['energy']), stdev(dataset['energy']), len(dataset['energy']))])
    summaries.append([(mean(dataset['key']), stdev(dataset['key']), len(dataset['key']))])
    summaries.append([(mean(dataset['loudness']), stdev(dataset['loudness']), len(dataset['loudness']))])
    summaries.append([(mean(dataset['mode']), stdev(dataset['mode']), len(dataset['mode']))])
    summaries.append([(mean(dataset['speechiness']), stdev(dataset['speechiness']), len(dataset['speechiness']))])
    del(summaries[-1])
    return summaries

summary = summarize_dataset(data)
