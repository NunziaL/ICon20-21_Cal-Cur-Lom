#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 15:32:41 2021

@author: antoniocurci
"""

import pandas as pd

#moduli privati
from byesian import classificatore_bayesiano
from spotify import canzoneDaSpotify
from supervised import previsione
from cluster import suggerimenti

import warnings
warnings.filterwarnings(action='ignore')

"Espressione regolare che cicla sui file della cartella con tutte le canzoni"
dfs = [pd.read_csv(f'archive/dataset-of-{decade}0s.csv') for decade in ['6', '7', '8', '9', '0', '1']]


for i, decade in enumerate([1960, 1970, 1980, 1990, 2000, 2010]):
    dfs[i]['decade'] = pd.Series(decade, index=dfs[i].index)

data = pd.concat(dfs, axis=0).sample(frac=1.0, random_state=1).reset_index(drop=True)

while(True):
    #prende in input il titolo della canzone
    ricerca = input("Dammi il titolo della canzone:")
    #prendere informazioni sulla canzone da Spotify
    song=canzoneDaSpotify(ricerca)
    track_predic = song.iloc[0]['track']
    artist_predic = song.iloc[0]['artist']
    if(type(song)!=int):
        break

#prepara la canzone alla predizione

songPredic=song.drop(['track', 'artist', 'uri'], axis=1)

#Classificazione canzone nella decade con classificatore Bayesiano
songPredic['decade']= classificatore_bayesiano(songPredic)
print("La decade di appartenenza della canzone è: ", int(songPredic.iloc[0]['decade']))

#previsione per ogni tipo di modello
result=previsione(data,songPredic)

a=songPredic['decade']
songPredic=songPredic.drop('decade', axis=1)
songPredic['target']=1
songPredic['decade']=a
print()
print("Canzoni simili: ")
songSugg = suggerimenti(songPredic, data)
for i in range(0, len(songSugg)):
    counter = i+1
    name_similar = songSugg[i]['track']
    artist_similar = songSugg[i]['artist']
    if (track_predic == name_similar) and (artist_predic == artist_similar):
        counter = counter-1
        continue
    else:
        print(counter,". " + name_similar + " - " + artist_similar)
    
    

