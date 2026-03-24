from api import lastfm
from utils import timestamploc

import time
import random
from datetime import datetime

def rescrobblefromList(scrobbleList, network):
    succesfulScrobbles = []
    progress = 1
    for scrobble in scrobbleList:
        chances = 0
        print('\n\nRescrobbling',scrobble['name'], int(progress/len(scrobbleList)*100),'%')
        while True:
            sucess = True
            initPlayCount = lastfm.getPlayCount()
            lastfm.scrobblebyParams(network, scrobble)
            if initPlayCount == lastfm.getPlayCount(): # the easiest way of verifying if the track was scrobbled is by checking if the playcount have changes!!1
                time.sleep(1)
                print('\nCouldn\'t scrobble at',datetime.fromtimestamp(scrobble['timestamp']), '\nRetrying...')
                match chances:
                    case 0: # first retry, generating a timestamp that is two weeks ago based on the old timestamp
                        scrobble['timestamp'] = timestamploc.generateNewTimeStampinXWeeksAgoUsingOldOne(scrobble['timestamp'],2)
                    case 1: # second retry, generating a time stamp that is one week ago based on the old timestamp
                        scrobble['timestamp'] = timestamploc.generateNewTimeStampinXWeeksAgoUsingOldOne(scrobble['timestamp'],1)
                    case 2: # third retry, generating a RANDOM time stamp that is at most one week ago
                        scrobble['timestamp'] = timestamploc.generateRandomTimeStampinXWeeksAgo(1)
                    case 3: # fourth retry, generating a RANDOM time stamp that is at most three days ago
                        scrobble['timestamp'] = timestamploc.generateRandomTimeStampinXDaysAgo(3)
                    case 4: # fifth retry, generating a RANDOM time stamp that is at most one day ago
                        scrobble['timestamp'] = timestamploc.generateRandomTimeStampinXDaysAgo(1)
                    case 5: # fuck off
                        print('\nCouldn\'t scrobble',scrobble['name'],'in any way... Jumping...')
                        sucess = False
                        break


                chances +=1
                continue
            pause =  random.randint(2, 10)
            if sucess:
                print('\nSucessfully scrobbled!\nWaiting for',pause,'seconds... I am (not) a robot...')
                succesfulScrobbles.append(scrobble)
            time.sleep(pause)
            break
        progress+=1
    return succesfulScrobbles