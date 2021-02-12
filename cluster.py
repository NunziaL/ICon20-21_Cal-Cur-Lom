# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 21:52:08 2021

@author: lomon
"""
from sklearn.cluster import KMeans
import joblib
import os

def creazioneCluster(data):
    train = data.drop(['track', 'artist', 'uri'], axis=1)
    if(os.path.exists('data/cluster.sav')):
        kmeans=joblib.load('data/cluster.sav')
    else:
        kmeans = KMeans(n_clusters=4000, random_state=0).fit(train)
        joblib.dump(kmeans,'data/cluster.sav')
    return kmeans

def suggerimenti(song, data):   
    
    kmeans=creazioneCluster(data)
    prediction = kmeans.predict(song)
    
    #cluster della canzone in input
    cluster_predetto = kmeans.cluster_centers_[prediction[0]]
    
    #selezione canzoni da suggerire
    songSugg = []
    for i in range(len(data)):
        if kmeans.labels_[i] == prediction[0]:
            songSugg.append(data.iloc[i])
    return songSugg
    