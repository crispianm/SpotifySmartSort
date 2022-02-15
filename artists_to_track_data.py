from configparser import ConfigParser
import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)

parser = ConfigParser()
parser.read('./spotify_credentials.cfg')

SPOTIPY_CLIENT_ID = parser.get('spotify', 'SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = parser.get('spotify', 'SPOTIPY_CLIENT_SECRET')

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET))

input = pd.read_csv('artists.csv', header = None)
artist_ids = []
for link in input[0]:
    
    artist_ids.append(link[32:54])

albums = []
album_track_ids = []

for artist_id in artist_ids:
    print('Searching for artist ' + artist_id)
    album_ids = []
    artist_uri = 'spotify:artist:' + artist_id

    # Add album ids to album_ids list
    results = sp.artist_albums(artist_uri, album_type='album')
    albums.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])
    for album in albums:
        album_ids.append(album['id'])

all_tracks = []
for id in album_ids:
    print('Searching for album ' + id)
    track_ids = []

    results = sp.album_tracks(id)
    tracks = results['items']
    all_tracks.extend(tracks)
    for track in tracks:
        track_ids.append(track['id'])

    album_track_ids.append(track_ids)

# Make sure the correct number of albums is in album_track_ids
assert len(album_track_ids) == len(albums)


# Remove unnecessary columns
columns_to_remove = ['analysis_url',
                    'type',
                    'uri',
                    'track_href']

# Add 4 new columns, album_title and artist
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


# Form empty dataframe with these columns
data = pd.DataFrame(columns=headings)


## Create DataFrames of features from track ids and compress them into lists so each album is one row in the data matrix
i = 0
j = 0
for album in album_track_ids:
    
    album_title = albums[i]['name']
    artist = albums[i]['artists'][0]['name']
    length = len(album)
    print('Looking up track information for ' + artist + ' - ' + album_title)

    for track in album:

        track_title = all_tracks[j]['name']

        results = sp.audio_features(track)
        if results[0]: 
            features = results[0]
        features_matrix = pd.DataFrame.from_records(features, index=[0])

        # Remove unneeded columns
        features_matrix.drop(columns = columns_to_remove, axis = 1, inplace = True)

        # Add track title
        features_matrix['track_title'] = track_title
        # Add album title
        features_matrix['album_title'] = album_title
        # Add artist name
        features_matrix['album_artist'] = artist
        # Add track number and total tracks
        features_matrix['track_number'] = all_tracks[j]['track_number']
        features_matrix['total_tracks'] = length

        # Add album as a row to the data df
        data = pd.concat([data, features_matrix])
        j += 1

    i += 1

# Remove duplicates
print('Removing duplicates...')
data.drop_duplicates(subset=['track_number', 'album_title', 'album_artist'])
data = data.reset_index(drop=True)
# data[~data.album_title.str.contains("remixes")]

# Save as csv
print('Saving as CSV\n')
data.to_csv('./data/data.csv')

print('Done')