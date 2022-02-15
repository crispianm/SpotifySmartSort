import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

client_id = 'db18963a66234a64a1038be650ec234d'
client_secret = 'fbbc842960094f07a0b4f0168a700604'
redirect_uri = 'http://localhost:8888/callback'

client = BackendApplicationClient(client_id=client_id)
oauth = OAuth2Session(client=client)
token = oauth.fetch_token(token_url='https://accounts.spotify.com/api/token', client_id=client_id, client_secret=client_secret)

# print(token)

### Gets a specific track from the API

# track = requests.get('https://api.spotify.com/v1/tracks/2gZ0PQd5J4iCjRrftwL5ov',
#     headers={'Authorization' : 'Bearer ' + token['access_token']})

# print(track)
# print(track.json())

### Gets audio features information of a specific track from the API

# features = requests.get('https://api.spotify.com/v1/audio-features',
#     headers={'Authorization' : 'Bearer ' + token['access_token']},
#     params={'ids' : '2gZ0PQd5J4iCjRrftwL5ov'})

# features = features.json()
# print(features)
# print(features['audio_features'][0]['danceability'])

### Doesn't work, gets the current user's profile from the API

# top = requests.get('https://api.spotify.com/v1/me', #/top/tracks', 
#         headers={'Authorization' : 'Bearer ' + token['access_token']})

# top = top.json()
# print(top)

### Gets a set of three albums from the API

albums = requests.get('https://api.spotify.com/v1/albums',
    headers={'Authorization' : 'Bearer ' + token['access_token']},
    params={'ids' : '5upt712ovrgK86j7tFBnvy,4y7T04fej3MJ8tAe2FeKD5,70kDwid3oC52MDbnRxWydm'})

albums = albums.json()
#print(albums)
for i in range(3):
    print(albums['albums'][i]['artists'][0]['name'])