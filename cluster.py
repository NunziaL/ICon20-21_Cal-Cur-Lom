# -*- coding: utf-8 -*-

from sklearn.cluster import KMeans
import joblib
import os

"""
Vengono creati 4000 cluster con l'algoritmo kmeans a partire dal dataset.
Sono eliminate le colonne 'track', 'artist', 'uri' in quanto non necessarie 
all'elaborazione del risultato. 
I cluster vengono salvati su un file .sav, in modo tale da non doverli creare 
ogni volta che il programma viene eseguito.
"""
def creazioneCluster(data):
    
    #Eliminazione degli attributi non necessari
    train = data.drop(['track', 'artist', 'uri'], axis=1)
    
    #Controllo se cluster già presenti su file
    if(os.path.exists('data/Cluster.sav')):
        kmeans=joblib.load('data/cluster.sav')
    else:
        kmeans = KMeans(n_clusters=4000, random_state=0).fit(train)
        joblib.dump(kmeans,'data/Cluster.sav')
    return kmeans

"""
Sono restituite le canzoni con simili caratterstiche a quella inserita dall'utente.
Viene predetto il cluster della canzone data in input, successivamente vengono 
trovate nel dataset le canzoni che appartengono allo stesso cluster e restituite in output
"""
def suggerimenti(song, data):   
    kmeans=creazioneCluster(data)
    
    #Predizione del cluster a cui appartiene la canzone
    prediction = kmeans.predict(song)
    
    #Selezione canzoni da suggerire
    songSugg = []
    for i in range(len(data)):
        if kmeans.labels_[i] == prediction[0]:
            songSugg.append(data.iloc[i])
    return songSugg
    