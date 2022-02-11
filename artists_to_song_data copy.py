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

for id in album_ids:
    print('Searching for album ' + id)
    track_ids = []

    results = sp.album_tracks(id)
    tracks = results['items']
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

# Add two new columns, album_title and artist
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
            'album_title',
            'album_artist']

# Form empty dataframe with these columns
data = pd.DataFrame(columns=headings)



## Create DataFrames of features from track ids and compress them into lists so each album is one row in the data matrix
i = 0
for album in album_track_ids:

    title = albums[i]['name']
    name = albums[i]['artists'][0]['name']

    print('Looking up track information for ' + name + ' - ' + title)

    features = []
    for track in album:
        results = sp.audio_features(track)
        # Empty data fix (Glass Animals)
        if results[0]: 
            features.append(results[0])

    features_matrix = pd.DataFrame.from_records(features)

    # Remove unneeded columns
    features_matrix.drop(columns = columns_to_remove, axis = 1, inplace = True)

    feature_lists = []
    for column in features_matrix:
        feature_lists.append(list(features_matrix[column]))

    # Add album title
    feature_lists.append(title)
    # Add artist name
    feature_lists.append(name)

    # Add album as a row to data df
    data.loc[i] = feature_lists
    i += 1

# Remove any duplicate albums that Spotify might've released multiple versions of
print('Removing duplicates...')
data.drop_duplicates(subset=['album_title', 'album_artist'])
# data[~data.album_title.str.contains("remixes")]

# Save as csv
print('Saving as CSV\n')
data.to_csv('./data/data.csv')

print('Done')