def evaluate_data(data):
    keyTransition = 0
    tempoTransition = 0
    trackNumTransition = 0
    loudnessTransition = 0
    timbreTransition = 0
    danceabilityTransition = 0
    energyTransition = 0
    speechinessTransition = 0
    acousticnessTransition = 0
    instrumentalnessTransition = 0
    livenessTransition = 0
    valenceTransition = 0
    # featureTransitionSum = 0

    for x in range(1,len(data)):
        # Select two songs for evaluation
        songA = data.iloc[x-1, :]
        songB = data.iloc[x, :]

        # Relative minor key conversion
        if songA.at['mode'] == 1:
            songA.at['key'] = (songA.at['key'] + 3) % 12
        if songB.at['mode'] == 1:
            songB.at['key'] = (songB.at['key'] + 3) % 12

        # Key Evaluation
        if songA['key'] == songB['key']:
            keyTransition += 1
        elif songA['key'] == (songB['key'] - 5) % 12 or songA['key'] == (songB['key'] + 5) % 12:
            keyTransition += 1

        # Tempo matching
        if songA['tempo'] * 0.9 <= songB['tempo'] <= songA['tempo'] * 1.1:
            tempoTransition += 1

        # Track order matching (for resorting albums only)
        if songB['track_number'] == songA['track_number'] + 1:
            trackNumTransition += 1

        # # Loudness matching the beginning and end of songs

        if songA['loudness_end'] * 0.7 <= songB['loudness_start'] <= songA['loudness_end'] * 1.3:
            loudnessTransition += 1
        elif songA['loudness'] * 0.7 <= songB['loudness'] <= songA['loudness'] * 1.3:
            loudnessTransition += 1

        # # Timbre matching the beginning and end of songs

        if songA['song_timbre_end'] * 0.7 <= songB['song_timbre_start'] <= songA['song_timbre_end'] * 1.3:
            timbreTransition += 1
        elif songA['song_timbre'] * 0.7 <= songB['song_timbre'] <= songA['song_timbre'] * 1.3:
            timbreTransition += 1

        # General feature matching to understand if the AI is matching similar features
        lowerLimit = 0.9
        upperLimit = 1.1

        if songA['danceability'] * lowerLimit <= songB['danceability'] <= songA['danceability'] * upperLimit:
            danceabilityTransition += 1
        if songA['energy'] * lowerLimit <= songB['energy'] <= songA['energy'] * upperLimit:
            energyTransition += 1
        if songA['speechiness'] * lowerLimit <= songB['speechiness'] <= songA['speechiness'] * upperLimit:
            speechinessTransition += 1
        if songA['acousticness'] * lowerLimit <= songB['acousticness'] <= songA['acousticness'] * upperLimit:
            acousticnessTransition += 1
        if songA['instrumentalness'] * lowerLimit <= songB['instrumentalness'] <= songA['instrumentalness'] * upperLimit:
            instrumentalnessTransition += 1
        if songA['liveness'] * lowerLimit <= songB['liveness'] <= songA['liveness'] * upperLimit:
            livenessTransition += 1
        if songA['valence'] * lowerLimit <= songB['valence'] <= songA['valence'] * upperLimit:
            valenceTransition += 1

    # Normalisation
    keyTransition = keyTransition / (len(data)-1)
    tempoTransition = tempoTransition / (len(data)-1)
    trackNumTransition = trackNumTransition / (len(data)-1)
    loudnessTransition = loudnessTransition / (len(data)-1)
    timbreTransition = timbreTransition / (len(data)-1)
    danceabilityTransition = danceabilityTransition / (len(data)-1)
    energyTransition = energyTransition / (len(data)-1)
    speechinessTransition = speechinessTransition / (len(data)-1)
    acousticnessTransition = acousticnessTransition / (len(data)-1)
    instrumentalnessTransition = instrumentalnessTransition / (len(data)-1)
    livenessTransition = livenessTransition / (len(data)-1)
    valenceTransition = valenceTransition / (len(data)-1)


    evaluation_vector = [keyTransition, tempoTransition, trackNumTransition, loudnessTransition,
                        timbreTransition, danceabilityTransition, energyTransition, speechinessTransition,
                        acousticnessTransition, instrumentalnessTransition, livenessTransition, valenceTransition]

    return evaluation_vector