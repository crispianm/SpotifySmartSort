from configparser import ConfigParser
import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np

parser = ConfigParser()
parser.read('./spotify_credentials.cfg')

SPOTIPY_CLIENT_ID = parser.get('spotify', 'SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = parser.get('spotify', 'SPOTIPY_CLIENT_SECRET')

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET))

user_id = 'czdoifmfngjhvoetavlok9dg5'
playlists = sp.user_playlists(user_id)
playlists = playlists['items']

playlist_id = '3YwPUeHZqBrFzLzP5BF8ND'

results = sp.playlist_tracks(playlist_id)
tracks = results['items']
track_ids = []
for track in tracks:
    track_ids.append(track['track']['id'])
track_ids

columns_to_remove = ['analysis_url', 'type', 'uri', 'track_href']
headings = ['danceability',
'energy',
'key',
'loudness',
'mode',
'speechiness',
'acousticness',
'instrumentalness',
'liveness',
'valence',
'tempo',
'id',
'duration_ms',
'time_signature',
'track_title',
'album_title',
'album_artist',
'track_number',
'total_tracks']

playlist_data = pd.DataFrame(columns=headings)

playlist_length = len(track_ids)

i = 0
for track in track_ids:
    results = sp.audio_features(track)
    if results[0]: 
        features = results[0]
    
    features_matrix = pd.DataFrame.from_records(features, index=[0])
    
    # Remove unneeded columns
    features_matrix.drop(columns = columns_to_remove, axis = 1, inplace = True)
    # print(features_matrix)

    # Add track title
    track_title = tracks[i]['track']['name']
    features_matrix['track_title'] = track_title

    # Add album title
    album_title = tracks[i]['track']['album']['name']
    features_matrix['album_title'] = album_title

    # Add artist name
    name = tracks[i]['track']['album']['artists'][0]['name']
    features_matrix['album_artist'] = name

    # Add track number and total tracks
    features_matrix['track_number'] = 0
    features_matrix['total_tracks'] = playlist_length

    # Add album as a row to the data df
    # print(features_matrix,'\n')
    # print(data)
    
    playlist_data = pd.concat([playlist_data, features_matrix])
    i += 1

playlist_data = playlist_data.reset_index(drop=True)
playlist_data.to_csv('./data/playlist_data.csv')

import random
random_order = random.sample(range(playlist_length), playlist_length)

# use model here
playlist_data['track_number'] = random_order
playlist_data = playlist_data.sort_values(by=['track_number'])

sorted_ids = list(playlist_data['id'])

# rearrange
from spotipy.oauth2 import SpotifyOAuth

scope = "playlist-modify-public"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,redirect_uri='http://localhost:5678/',client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET))

UPDATED_PLAYLIST = sp.playlist_replace_items(playlist_id,sorted_ids)
UPDATED_PLAYLIST
