import requests
import spotipy
import os
import re
import sys
import json
import spotipy.util as util
from json.decoder import JSONDecodeError

# Get the username from terminal
username = sys.argv[1]

# Fix scope maybe
scope = 'user-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private'

try:
    token = util.prompt_for_user_token(username, scope)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope)

spotify = spotipy.Spotify(auth=token)

#print(json.dumps(name, sort_keys=True, indent=4))
description = "The King and Queen had 2 daughters. Their names were Olivia and Emerald"
words = ['The', 'King', 'and', 'Queen', 'had', '2', 'daughters', 'Their', 'names',
          'were', 'Olivia', 'and', 'Emerald']

searches = []       # an array of search entries
songs = []          # an array of songs objects

# (string) title:       song title (does not include any words included inside brackets ())
# (string) search:      the corresponding search keywords that found this song title
# (array) searchSplit:  the corresponding search keywords parsed into an array of individual words
# (int) rank:           a number value that demonstrates how closely the title matches the search entry
class Song(object):
    title = ""
    search = ""
    searchSplit = []
    rank = 0

# splits a search
def splitSearch(search):
    return search.split()

# removes brackets from a song
def removeBrackets(song):
    split = song.split("(")
    altered_song = split[0]
    return altered_song

# generate 4 search entries
def findSearches(fourWordsArray):
    #searches = [] # should empty searches array everytime findSearches is called
    for i in range(4):

        # gets the first one word search
        if i == 0:
            search = fourWordsArray[i]
            prevSearch = search
            searches.append(search)

        # finds two, three and four word searches by combining the words together
        else:
            search = prevSearch + " " + fourWordsArray[i]
            prevSearch = search
            searches.append(search)

    print(searches)

# Finds the searchResults for 4 words at a time
# Calls findSearches
def findSearchResults(descript):
    fourWordsArray = descript[:4]
    findSearches(fourWordsArray)

    for search in searches:
        results = spotify.search(q='track:' + search, type='track') # do the search
        index = len(results['tracks']['items']) # index = number of search results
        searchSplit = splitSearch(search)

        # for each song from the search, create a song, an add the corresponding search to the array
        for x in range(index):
            song = Song()
            name = results['tracks']['items'][x]['album']['name']
            song.title = removeBrackets(name)
            song.search = search
            song.searchSplit = searchSplit
            songs.append(song)

            #print("Title: ", song.title, "Search: ", song.search, "Search Split: ", song.searchSplit, song.rank)

def rankTitles():
    for song in songs:
        searchWords = song.searchSplit
        for word in searchWords:
            if word in song.title:
                song.rank += 1



# Find the closest title from one list
def findBestTitle():
    temp = []
    #currentSongs = potentialSongs[index] # the current song list that we're working with
    i = 0
    for search in searchesSplit:
        #term = search
        length = len(search)
        print(length)
        for word in search:
            print(word)
        '''
        if length == 1: # if the term has only one word
            print("One Term")
        else:
            print("Many Terms")
        '''
        i += 1

def main():
    findSearchResults(words)
    rankTitles()
    for song in songs:
        print(song.title, song.rank, song.search)
        #print("Title: ", song.title, "Search: ", song.search, "Search Split: ", song.searchSplit, song.rank)
    #findBestTitle()

main()
