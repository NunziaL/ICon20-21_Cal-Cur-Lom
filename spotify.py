#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

"""
Prende la canzone dal database di spotify
"""
def canzoneDaSpotify(ricerca):
    cid = 'c1f44332d14943bd9766a095aab44a37'
    secret = '7b12a556717a4b17bbfcc7f19f4bf3d9'
    
    #accesso all'account Developer su Spotify
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    #trova la canzone dal titolo. limit è il numero di risultati
    songSp = sp.search(ricerca, limit=1, type="track")
    if(songSp['tracks']['items']==[]):
        return None
    else:
        #prende l'URI della canzone
        uriSong = songSp['tracks']['items'][0]['uri']
        
        #prendere le features della canzone
        feature = sp.audio_features(uriSong)[0]
        analysis= sp.audio_analysis(uriSong)

        lst = {'track': songSp['tracks']['items'][0]['name'],
               'artist': songSp['tracks']['items'][0]['artists'][0]['name'],
               'uri': songSp['tracks']['items'][0]['uri'],
               'danceability':[feature['danceability']],
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
               'sections':[len(analysis["sections"])]}
        
        song = pd.DataFrame(lst)
        return song
  
"""
Attraverso il nome della canzone acquisito sotto forma di stringa, prende l'URL della canzone
"""
def getUrl(ricerca):
    cid = 'c1f44332d14943bd9766a095aab44a37'
    secret = '7b12a556717a4b17bbfcc7f19f4bf3d9'
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    songSp = sp.search(ricerca, limit=1, type="track")
    urlSong = songSp['tracks']['items'][0]['external_urls']['spotify']
    return urlSong