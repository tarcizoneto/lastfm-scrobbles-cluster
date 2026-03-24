def getTagsfromTitle(songname:str):
    songname = songname.lower()
    if songname.startswith('(') and ") " in songname:
        songname = songname.split(') ')[1]
    if songname.startswith('[') and "] " in songname:
        songname = songname.split('] ')[1]
    
    if ' - ' in songname:
        return songname.split(' - ')[-1]

    if " (" in songname:
        if " [" in songname:
            return songname.split(' [')[-1].replace(']', '')
        return songname.split(' (')[-1].replace(')','')
    
    return None

def makeSongNamebeReadyforFilter(songname:str):  # avoid possible sensitive case errors, and (live) [feat] things
    songname = songname.lower()
    if songname.startswith('(') and ") " in songname:
        songname = songname.split(') ')[1]
    if songname.startswith('[') and "] " in songname:
        songname = songname.split('] ')[1]
    #songname = songname.replace(' - ', '').replace('(', '').replace(')', '').replace('[', '').replace(']', '')

    # if len(songname.split(' - ')) > 1:
    #     songname = songname.split(' - ')[0]
    return songname.split('(')[0].split('[')[0].split(' - ')[0]
    #return songname   

def filterDuplicatedTracks(recentDatabase, topDatabase : dict, how='name'):
    processedDatabaseDict = []

    match how:
        case 'name': # tries to find duplicate songs by catching repeated songnames / words in different songs and including the same artist
            for song in recentDatabase:
                currentTrackName = song['name']
                currentTrackArtist = song['artist']
                duplicateFiltering = list(filter(
                    lambda track: 
                    track['artist'] in currentTrackArtist # the track NEEDS to be of the same artist's creation, or else it will try to find words in every artists' tracks
                    and
                    makeSongNamebeReadyforFilter(track['name']) in currentTrackName.lower()
                    and getTagsfromTitle(track['name']) == getTagsfromTitle(currentTrackName.lower()), # check if the song tags are equal, so we don't rescrobble song that, for example, a live version in a studio version
                    topDatabase
                    ))
                if len(duplicateFiltering) > 1: # if it has filtered and theres more than 2 songs in the array, that means that its duplicated and theres 2 "versions"
                    print('\n\nOops! Duplicated song founded: ', currentTrackName, ', see: \n')
                    masterName = duplicateFiltering[0]['name'].lower()
                    masterTags = getTagsfromTitle(masterName)
                    for duplicato in duplicateFiltering:
                        currentDuplicatoName = duplicato['name'].lower()
                        
                        print(duplicato['name'],':',duplicato['playcount'])
                        # as the filter still filters songnames wrongly as in "AMEN" is a "duplicate" of "FLAMENCO", it is better rechecking if the each names are equal to eachother
                        if masterTags == None and masterName != currentDuplicatoName: # and as the tagged songs filter better with eachother, we don't have to re-check them
                            print('Re-oops, the names don\'t match... reducing', currentDuplicatoName)
                            duplicateFiltering.remove(duplicato)
                    if len(duplicateFiltering) < 2:
                        print('\nThere aren\'t any duplicated tracks in', masterName,', passing...')
                        continue
                    if duplicateFiltering in processedDatabaseDict:
                        print('Duplicate already detected!\n')
                        continue
                    processedDatabaseDict.append(duplicateFiltering)
                        
                
    
    return processedDatabaseDict

def filterTrackScrobbleHistoryfromRecentTracksbyUrl(url, playcount, recentTracks):
    processedList = list(filter(lambda scrobble:
                scrobble['url'] == url,
                recentTracks
                ))
    print('\n\nFound',len(processedList),'scrobbles from a total of',playcount)
    # if len(processedList) < playcount-3:
    #     raise 
    return processedList

def createScrobbleListfromDuplicatosandRecent(duplicatosList : list, recentTracks : list):

    toScrobble = []
    for duplicato in duplicatosList:
        masterScrobble = duplicato[0]
        for track in duplicato[1:]:
            for scrobble in filterTrackScrobbleHistoryfromRecentTracksbyUrl(track['url'], int(track['playcount']), recentTracks):
                toScrobble.append({'name': masterScrobble['name'], 'artist': masterScrobble['artist'], 'mbid': masterScrobble['mbid'], 'timestamp': int(scrobble['uts'])+6})
                
                # print('Scrobbling at', datetime.fromtimestamp(int(scrobble['uts'])), ':\n', masterScrobble['name'],'--', masterScrobble['artist'], '; \nMessed name/artist:\n', track['name'], '--', track['artist'])

            print('Added to queue: ', track['playcount'],'scrobbles to',masterScrobble['name'])
            # time.sleep(2)
    return toScrobble

