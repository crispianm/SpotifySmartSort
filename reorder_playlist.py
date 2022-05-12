from configparser import ConfigParser
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import MinMaxScaler


def get_timbre(song):

    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from sklearn.preprocessing import MinMaxScaler

    headings = [
        "start",
        "duration",
        "confidence",
        "loudness",
        "tempo",
        "tempo_confidence",
        "key",
        "key_confidence",
        "mode",
        "mode_confidence",
        "time_signature",
        "time_signature_confidence",
    ]
    segment_data = pd.DataFrame(columns=headings)

    pitches = []
    timbres = []

    track_segments = sp.audio_analysis(song)["segments"]

    # Extract pitch and timbre data from track
    for results in track_segments:
        pitches.append(results.get("pitches"))
        del results["pitches"]
        timbres.append(results.get("timbre"))
        del results["timbre"]

    # Add track segment data to dataframe
    for results in track_segments:

        if results:
            features = results

        segment_features_matrix = pd.DataFrame.from_records(features, index=[0])

        # Add additional data features from input data
        segment_features_matrix["track_title"] = playlist_data_full["track_title"]
        segment_features_matrix["album_title"] = playlist_data_full["album_title"]
        segment_features_matrix["album_artist"] = playlist_data_full["album_artist"]
        # segment_features_matrix['order'] = playlist_data_full.iloc[i,20]

        segment_data = pd.concat([segment_data, segment_features_matrix])
        # segment_data = segment_data.append(segment_features_matrix)

    # # Delete empty rows of dataframe
    # for row in range(segment_data.shape[0]-1,0,-1):
    #     if segment_data.iloc[row,10] == 0:
    #         segment_data.drop(row, inplace=True)

    # Add pitch and timbre data
    segment_data["pitches"] = pitches
    segment_data["timbres"] = timbres
    # segment_data.to_csv('./data/segments_end.csv')

    # Import data
    # segmentData = pd.read_csv("./data/Sam/all_segments.csv")
    segmentData = pd.DataFrame(segment_data)

    # Remove irrelevent columns
    segmentColumnsToRemove = ["loudness_end", "confidence"]  #'track_title'
    segmentData.drop(columns=segmentColumnsToRemove, axis=1, inplace=True)

    # Convert Track Title to unique number
    segmentTrackTitles = segmentData["track_title"].astype(
        "category"
    )  # Extract the song title column
    segmentDataCodes = (
        segmentTrackTitles.cat.codes
    )  # Assign each song title to a unique number
    segmentData[
        "track_title"
    ] = segmentDataCodes  # Replace track title with unique number

    # Initialise output matrix
    allSongEuclidianTimbreHeadings = [
        "song_timbre",
        "song_timbre_start",
        "song_timbre_end",
        "loudness_start",
        "loudness_end",
    ]
    allSongEuclidianTimbre = pd.DataFrame(
        np.zeros((max(segmentDataCodes), 5)), columns=allSongEuclidianTimbreHeadings
    )

    songSegmentData = segmentData  # .loc[segmentData['track_title'] == song] # Extract segments for one song

    # Find number of segments in first 10 secs of song
    time = 0
    numStartSegments = 0
    while time < 10:
        time += songSegmentData.iloc[numStartSegments, 1]
        numStartSegments += 1

    # Find number of segments in last 10 secs of song
    time = 0
    numEndSegments = 0
    while time < 10:
        time += songSegmentData.iloc[-numStartSegments, 1]
        numEndSegments += 1

    # Timbre
    timbreStr = songSegmentData[
        "timbres"
    ]  # Extract Timbre column vector from segmentData
    timbre = pd.DataFrame(timbreStr.tolist())

    # Weight timbre dimensions in order accourding to importance
    weightedTimbre = pd.DataFrame(np.zeros((len(timbre), 12)))
    for x in range(1, 12):
        weightedTimbre[x] = timbre[x] * (0.9**x)

    # For each row of timbre values find the euclidean distance of the 12 variables
    euclidianTimbre = pd.DataFrame(np.zeros((1, len(timbre))))
    for x in range(len(timbre)):
        euclidianTimbre[x] = np.linalg.norm(weightedTimbre.loc[x, :])
    euclidianTimbre = euclidianTimbre.transpose()

    # Normalise the data between zero and one
    euclidianTimbre = pd.DataFrame(
        MinMaxScaler(feature_range=(0, 1)).fit_transform(euclidianTimbre)
    )
    # euclidianTimbre.plot.line()

    # Average for euclidian distance for song
    euclidianTimbreSong = float(np.mean(euclidianTimbre, axis=0))
    # Average for the first 10 secs of the song
    euclidianTimbreSongStart = float(
        np.mean(euclidianTimbre.head(numStartSegments), axis=0)
    )
    # Average for the last 10 secs of the song
    euclidianTimbreSongEnd = float(
        np.mean(euclidianTimbre.tail(numEndSegments), axis=0)
    )

    # Loudness
    songLoudness = songSegmentData["loudness_max"]
    # Average for the first 10 secs of the song
    loudnessSongStart = float(np.mean(songLoudness.head(numStartSegments), axis=0))
    # Average for the last 10 secs of the song
    loudnessSongEnd = float(np.mean(songLoudness.tail(numEndSegments), axis=0))

    allSongEuclidianTimbre.loc[0] = [
        euclidianTimbreSong,
        euclidianTimbreSongStart,
        euclidianTimbreSongEnd,
        loudnessSongStart,
        loudnessSongEnd,
    ]  # Export values

    return allSongEuclidianTimbre


parser = ConfigParser()
parser.read("./spotify_credentials.cfg")

SPOTIPY_CLIENT_ID = parser.get("spotify", "SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = parser.get("spotify", "SPOTIPY_CLIENT_SECRET")

sp = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET
    )
)

user_id = "czdoifmfngjhvoetavlok9dg5"
playlists = sp.user_playlists(user_id)
playlists = playlists["items"]


playlist_id = "3YwPUeHZqBrFzLzP5BF8ND"


results = sp.playlist_tracks(playlist_id)
tracks = results["items"]
track_ids = []
for track in tracks:
    track_ids.append(track["track"]["id"])
track_ids

columns_to_remove = ["analysis_url", "type", "uri", "track_href"]
headings = [
    "danceability",
    "energy",
    "key",
    "loudness",
    "mode",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
    "id",
    "duration_ms",
    "time_signature",
    "track_title",
    "album_title",
    "album_artist",
    "track_number",
    "total_tracks",
]

playlist_data = pd.DataFrame(columns=headings)

playlist_length = len(track_ids)

i = 0
for track in track_ids:
    results = sp.audio_features(track)
    if results[0]:
        features = results[0]

    features_matrix = pd.DataFrame.from_records(features, index=[0])

    # Remove unneeded columns
    features_matrix.drop(columns=columns_to_remove, axis=1, inplace=True)
    # print(features_matrix)

    # Add track title
    track_title = tracks[i]["track"]["name"]
    features_matrix["track_title"] = track_title

    # Add album title
    album_title = tracks[i]["track"]["album"]["name"]
    features_matrix["album_title"] = album_title

    # Add artist name
    name = tracks[i]["track"]["album"]["artists"][0]["name"]
    features_matrix["album_artist"] = name

    # Add track number and total tracks
    features_matrix["track_number"] = tracks[i]["track"]["track_number"]
    features_matrix["total_tracks"] = playlist_length

    # Add album as a row to the data df
    # print(features_matrix,'\n')

    playlist_data = pd.concat([playlist_data, features_matrix])
    i += 1

playlist_data = playlist_data.reset_index(drop=True)
# playlist_data.to_csv('./data/playlist_data.csv')
playlist_data_full = pd.DataFrame(playlist_data)

timbre = pd.DataFrame(
    columns=[
        "song_timbre",
        "song_timbre_start",
        "song_timbre_end",
        "loudness_start",
        "loudness_end",
    ]
)

i = 0
for track in track_ids:
    print("Getting timbre for: " + track)
    track_timbre = get_timbre(track)
    timbre = pd.concat([timbre, track_timbre], axis=0)
    print("Timbre obtained.\n")

# playlist_data = pd.concat([playlist_data, timbre], axis=0)
timbre = timbre.reset_index(drop=True)

playlist_data = pd.concat([playlist_data, timbre], axis=1)


# Remove unnecessary testing columns
columns_to_remove = [
    "id",
    "track_title",
    "album_title",
    "album_artist",
    "track_number",
    "total_tracks",
    "key",
    "mode",
    "duration_ms",
    "time_signature",
]
playlist_data.drop(columns=columns_to_remove, axis=1, inplace=True)


# get permissions to rearrange
from spotipy.oauth2 import SpotifyOAuth

scope = "playlist-modify-public"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scope,
        redirect_uri="http://localhost:5678/",
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
    )
)

## Load trained model
model = pickle.load(
    open("./regression/MODEL.sav", "rb")
)  # change to whichever model we want to use
playlist_data_full["order"] = model.predict(playlist_data.values)
playlist_data_full = playlist_data_full.sort_values(by=["order"])
# playlist_data_full['order'] = np.arange(1, playlist_data_full.shape[0]+1) # convert order to integer playlist track number


# rearrange
sorted_ids = list(playlist_data_full["id"])

UPDATED_PLAYLIST = sp.playlist_replace_items(playlist_id, sorted_ids)
UPDATED_PLAYLIST
