from api import lastfm, rescrobbler
from utils import jsonloc, listmanipulationloc
from utils import timestamploc

import os

TOPTRACKS_FILE = 'data/topTracks.json'
RECENTTRACKS_FILE = 'data/recentTracks.json'
GUIDE = input("Do you want for me to pause in every step? (y/n)...").strip().lower() == "y"

network = lastfm.authenticate()

# get user's top tracks (useful for realizing which duplicate is better to rescrobble)
# and checking the modification time, so it can recreate it if it is too old
if not os.path.exists(TOPTRACKS_FILE) or os.path.getmtime(TOPTRACKS_FILE) < timestamploc.NOW - 3*timestamploc.DAY:
    print('Creating top tracks database!..')
    topdatabase = lastfm.createDatabasefromTopTracks(network)
else:

    topdatabase = jsonloc.loadJson(TOPTRACKS_FILE)
    print('Top tracks database already created!')


if GUIDE:
    input('Done! Do you want to continue to recentTracks gather?.. (Press Enter)')


# get user's recent tracks (useful for gathering the scrobble history of the duplicate track and try to rescrobble it in a reali)
if not os.path.exists(RECENTTRACKS_FILE):
    print('Creating recent tracks database!..')
    recentdatabase = lastfm.createDatabasefromRecentTracks(network)
else: # acknowledge the file creation datetime and grab recent tracks since its creation, that is, don't rescrobble tracks that were already "fixed"
    recentdatabase = lastfm.createDatabasefromRecentTracks(network, os.path.getmtime(RECENTTRACKS_FILE))


if GUIDE:
    input('Done! Do you want to continue to duplicate tracks filtering?.. (Press Enter)')

print('Starting duplicated tracks filtering...')
duplicatedDict = listmanipulationloc.filterDuplicatedTracks(recentdatabase, topdatabase, 'name')
print('Filtering done!')

if GUIDE:
    input('Done! Do you want to continue to scrobble list creation?.. (Press Enter)')

print('Creating scrobble list...')
scrobbleList = listmanipulationloc.createScrobbleListfromDuplicatosandRecent(duplicatedDict, recentdatabase)


# sorting scrobbles by their scrobble date and time, to try making a logically rescrobbling (older to new)
# it is not really useful SOMETIMES, as for example, when the scrobbles are really old, because the date time is randomly generated
scrobbleList.sort(key=lambda x: x['timestamp'])

if GUIDE:
    input('Almost all done! Do you want to start rescrobbling?.. (Press Enter)')


print('\n\n\n\nDone!\nRescrobbled', len(rescrobbler.rescrobblefromList(scrobbleList, network)), 'times of', len(scrobbleList))
input('Press Enter to close...')


# NOTES
# we CANNOT recreate the scrobble at its old timestamp, we only can scrobble them at least two weeks ago (i've tested it...)
# so it will create a strange history if you will run this at once and clean your all time history
# do NOT erase any json file, even if they look temporary-ish