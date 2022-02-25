[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-f059dc9a6f8d3a56e377f745f24479a46679e63a5d9fe6f495e02850cd0d8118.svg)](https://classroom.github.com/online_ide?assignment_repo_id=6799724&assignment_repo_type=AssignmentRepo)
# Spotify SmartSort
## Setup
### Training Data
Fetch spotify API song analysis for songs in training albums:

    Normalise features
        Danceability, Energy, Normalised Loudness, Speechiness, Acousticness, 
        Instrumentalness, Liveness, Valence, Normalised Tempo, Track Number/Total Albums
    Analysis 
        Timbre - first & last 10 secs of song, and song average
        Loudness - first & last 10 secs of song
For each training data point, save the above data for the song and the previous & next songs in the album.
### Clustering
Group data into bins
### Tune test data
Fall out tree - to weight the most important variables.
### Auto Encoder
Dimensionality reduction
### AI Training
Given song data, predict song data for next & previous song.

    NN    or    Regression
### Auto Decoder
To out

## Usage
Get playlist to sort.

Choose random first song.
### Simple Algorithm
Find most likely next song for best transistion.
(K-nearest neighbours)

Repeat for all songs in the playlist, and save to spotify.

Visualisation - Graph the probabilities of most likely next songs 
### Optimised Algorithm
Maximise the summation of probabilities for all transistions in the playlist (so the end of the playlist dosen't have a few songs with horrible transistions).

Visualisation - Graph the strength of transitions of the playlist