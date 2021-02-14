# -*- coding: utf-8 -*-

import pandas as pd

#moduli privati
from byesian import classificatore_bayesiano
from spotify import canzoneDaSpotify
from supervised import previsione
from cluster import suggerimenti

import warnings
warnings.filterwarnings(action='ignore')

#Espressione regolare che apre i file della cartella con tutte le canzoni per ogni decade salvando le informazioni in un dataframe
dfs = [pd.read_csv(f'archive/dataset-of-{decade}0s.csv') for decade in ['6', '7', '8', '9', '0', '1']]

#Aggiunta della colonna decade al dataset
for i, decade in enumerate([1960, 1970, 1980, 1990, 2000, 2010]):
    dfs[i]['decade'] = pd.Series(decade, index=dfs[i].index)

data = pd.concat(dfs, axis=0).sample(frac=1.0, random_state=1).reset_index(drop=True)

while(True):
    #Prende in input il titolo della canzone
    ricerca = input("Dammi il titolo della canzone:")
    #Prende informazioni sulla canzone da Spotify 
    song=canzoneDaSpotify(ricerca)
    track_predic = song.iloc[0]['track']
    artist_predic = song.iloc[0]['artist']
    if(type(song)!=int):
        break

#Prepara la canzone alla predizione eliminando gli attributi non necessari
songPredic=song.drop(['track', 'artist', 'uri'], axis=1)

#Classificazione canzone nella decade con classificatore Bayesiano
songPredic['decade']= classificatore_bayesiano(songPredic)
print("La decade di appartenenza della canzone è: ", int(songPredic.iloc[0]['decade']))

#Previsione per ogni tipo di modello
result=previsione(data,songPredic)

#Aggiunge valore alla colonna target in base al valore preponderante nelle predizioni
count1 = 0
count0 = 0
for model in result.values():
    if model == 1:
        count1 = count1 + 1
    else:
        count0 = count0 + 1
if count1 > count0:
    songPredic['target'] = 1
else:
    songPredic['target'] = 0
    
#Aggiunta della decade nella colonna corrispondente   
a=songPredic['decade']
songPredic=songPredic.drop('decade', axis=1)
songPredic['decade']=a
print()

#Stampa delle canzoni simili a quella inserita dall'utente
print("Canzoni simili: ")
songSugg = suggerimenti(songPredic, data)
for i in range(0, len(songSugg)):
    counter = i+1
    name_similar = songSugg[i]['track']
    artist_similar = songSugg[i]['artist']
    if (track_predic == name_similar) and (artist_predic == artist_similar):
        counter = counter - 1
        continue
    else:
        print(counter,". " + name_similar + " - " + artist_similar)
    
    

