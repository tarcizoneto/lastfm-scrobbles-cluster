from datetime import datetime
from urllib.parse import urlparse, parse_qs
from utils import jsonloc


import pylast
import os
import requests
import time
import webbrowser
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
USERNAME = os.getenv('USERNAME')
SESSION_KEY_FILE = os.path.join(os.path.expanduser("~"), ".session_key")


print(API_KEY)
print(API_SECRET)
print(USERNAME)

def authenticate():
    # we are authenticating here, this function exists to prepare pylast on correctly using lastfm's api
    
    network = pylast.LastFMNetwork(API_KEY, API_SECRET)
    if not os.path.exists(SESSION_KEY_FILE): # check if there already is a session key in user's file
        skg = pylast.SessionKeyGenerator(network)
        url = skg.get_web_auth_url()

        print(f"Please authorize this script to access your account: {url}\n")
        

        webbrowser.open(url)
        parsed = urlparse(url)
        token = parse_qs(parsed.query)["token"][0]
        print('Authenticating...')

        while True:
            try:
                
                session_key = skg.get_web_auth_session_key(url)
                with open(SESSION_KEY_FILE, "w") as f:
                    f.write(session_key)
                break
            except pylast.WSError:
                time.sleep(1)
    else:
        session_key = open(SESSION_KEY_FILE).read()

    # network.session_key = session_key
    network = pylast.LastFMNetwork(api_key=API_KEY,api_secret=API_SECRET,session_key=session_key, username=USERNAME)
    print('Authenticated! Connected user: ',network.get_authenticated_user().get_name())
    return network


def requestMethodsfromHTTP(method:str, limit=0, page=0, from_timestamp=0): #as the pylast doesnt care about their users paging in gettoptracks method, we need to grab it using requests
    while True:
        grab = requests.get("http://ws.audioscrobbler.com/2.0/", params={
            "method": method,
            "user": USERNAME,
            "api_key": API_KEY,
            "format": "json",
            "limit": limit,
            "page": page,
            "from": int(from_timestamp)
        })
        try:
            grab.raise_for_status()
        except: # if something goes wrong and its not the user's fault (status > 500)
            if grab.status_code < 500:
                grab.raise_for_status()
            print("I'm sorry, something went wrong with the API, retrying in 6 seconds... Status:", str(grab.status_code))
            time.sleep(6)
            continue
        parsedGrab = grab.json()
        if "error" in parsedGrab:
            raise ValueError
        return parsedGrab


def getPlayCount():
    return int(requestMethodsfromHTTP('user.getInfo')['user']['playcount'])

def createDatabasefromTopTracks(network : pylast.LastFMNetwork): # criar um (talvez, nao sei ainda) json, ou ate um dicionario no proprio script com todas as tracks e separadas com cada uma de suas contagens de scrobbles, para poder comparar mais eficientemente
    print('Gathering user...')
    user = network.get_authenticated_user()
    print('Gathering top tracks\' master...')
    gatherPageIdx = 1
    database = []
    # get the first grab and save its attributes, and use its grab to start appending the database
    fGrab = requestMethodsfromHTTP("user.getTopTracks", 350,1)
    totalPages = int(fGrab["toptracks"]["@attr"]["totalPages"])

    for song in fGrab["toptracks"]["track"]:
        print('Appending: '+song['name'])
        database.append({'name': song['name'], 'artist': song['artist']['name'], 'mbid': song['mbid'], 'playcount': int(song['playcount']), 'url': song['url']}) # recreating the dict with only necessary things from grab

    while True:
        print('Gathering top tracks; Current page: ',gatherPageIdx, '\nTracks gathered: ',gatherPageIdx*350, 'of ~'+str(totalPages*350),'tracks')
        gatherPageIdx += 1 # iterating...

        grab = requestMethodsfromHTTP("user.getTopTracks", 350,gatherPageIdx)

        for song in grab["toptracks"]["track"]:
            print('Appending: '+song['name'])
            # print({'name': song['name'], 'artist': song['artist']['name'], 'mbid': song['mbid'], 'playcount': song['playcount'], 'url': song['url']})
            database.append({'name': song['name'], 'artist': song['artist']['name'], 'mbid': song['mbid'], 'playcount': int(song['playcount']), 'url': song['url']}) # recreating the dict with only necessary things from grab

        
        if gatherPageIdx >= totalPages:
            jsonloc.dumpJson('data/topTracks.json', database)
            print('Done! Saved in data/toptracks.json','\nTracks gathered: ',len(database))
            break
        time.sleep(3) # just so you don't get banned :)
    
    return database


def createDatabasefromRecentTracks(network : pylast.LastFMNetwork, from_timestamp=0):
    print('Gathering user...')
    user = network.get_authenticated_user()
    print('Gathering recent tracks\' master...')
    gatherPageIdx = 1
    database = []
    # get the first grab and save its attributes, and use its grab to start appending the database
    fGrab = requestMethodsfromHTTP("user.getRecentTracks", 1000,1, from_timestamp)
    totalPages = int(fGrab["recenttracks"]["@attr"]["totalPages"])

    for song in fGrab["recenttracks"]["track"]:
        print('Appending: '+song['name'], song['date']['uts'])
        database.append({'name': song['name'], 'artist': song['artist']['#text'], 'mbid': song['mbid'], 'uts': int(song['date']['uts']), 'url': song['url']}) # recreating the dict with only necessary things from grab

    while True:
        print('Gathering recent tracks; Current page: ',gatherPageIdx, '\nTracks gathered: ',gatherPageIdx*1000,'of ~'+str(totalPages*1000),'tracks')
        gatherPageIdx += 1 # iterating...

        grab = requestMethodsfromHTTP("user.getRecentTracks", 1000,gatherPageIdx, from_timestamp)

        for song in grab["recenttracks"]["track"]:
            print('Appending: '+song['name'], song['date']['uts'])
            # print({'name': song['name'], 'artist': song['artist']['name'], 'mbid': song['mbid'], 'playcount': song['playcount'], 'url': song['url']})
            database.append({'name': song['name'], 'artist': song['artist']['#text'], 'mbid': song['mbid'], 'uts': int(song['date']['uts']), 'url': song['url']})

        
        if gatherPageIdx >= totalPages:
            jsonloc.dumpJson('data/recentTracks.json', database)
            print('Done! Saved in data/recenttracks.json','\nTracks gathered: ',len(database))
            break
        time.sleep(5) # just so you don't get banned :)
    
    return database


def scrobblebyParams(network:pylast._Network,params):
    while True:
        try:
            network.scrobble(artist=params['artist'],title=params['name'],timestamp=int(params['timestamp']))
            print('Scrobbling... ('+str(datetime.fromtimestamp(params['timestamp']))+')')
            break
        except pylast.WSError as e:
                print(e.details)
                continue
        

