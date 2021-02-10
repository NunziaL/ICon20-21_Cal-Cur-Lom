# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 20:57:19 2021

@author: lomon
"""

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
analysis = sp.audio_features(uriSong)[0]

import pandas as pd
lst = {'danceability':[analysis['danceability']],
       'energy':[analysis['energy']],
       'key':[analysis['key']],
       'loudness':[analysis['loudness']],
       'mode':[analysis['mode']],
       'speechiness':[analysis['speechiness']],
       'acousticness':[analysis['acousticness']],
       'instrumentalness':[analysis['instrumentalness']],
       'liveness':[analysis['liveness']],
       'valence':[analysis['valence']],
       'tempo':[analysis['tempo']],
       'duration_ms':[analysis['duration_ms']],
       'time_signature':[analysis['time_signature']],
       'chorus_hit':[0],
       'sections':[0], 
       'decade':[2010]}
X = pd.DataFrame(lst)

    