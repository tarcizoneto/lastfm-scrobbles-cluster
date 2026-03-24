import time
import random

MONTH = 30*24*60*60
WEEK = 7*24*60*60
DAY = 24*60*60
NOW = int(time.time())

def generateNewTimeStampinXWeeksAgoUsingOldOne(oldTs, weeks):
    NOW = int(time.time())
    thisWeekStart = NOW - NOW%WEEK - weeks*WEEK
    timePassedSinceOldTsWeekStart = oldTs%WEEK
    newTs = thisWeekStart + timePassedSinceOldTsWeekStart # keeping the old weekday, but in x weeks ago
    if newTs > NOW: # if the generated timestamp is in the future, make it go back a week
        newTs -= WEEK
    print('Generated:',int((NOW-newTs)/24/60/60),'days ago')
    return newTs

def generateRandomTimeStampinXWeeksAgo(weeks):
    NOW = int(time.time())
    newTs = NOW-random.randint(0,weeks*WEEK)
    print('Generated (random):',int((NOW-newTs)/24/60/60),'days ago')
    return newTs

def generateRandomTimeStampinXDaysAgo(days):
    NOW = int(time.time())
    newTs = NOW-random.randint(0,days*DAY)
    print('Generated (random):',int((NOW-newTs)/60/60),'hours ago')
    return newTs
