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

# Need a function that parses a string into an array
description = "The King and Queen had 2 daughters. Their names were Olivia and Emerald"
words = ['The', 'King', 'and', 'Queen', 'had', '2', 'daughters', 'Their', 'names',
          'were', 'Olivia', 'and', 'Emerald']

#print(json.dumps(name, sort_keys=True, indent=4))
searches = [] # an array of search entries
potentialSongs = [] # an array of lists of search results

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

    #print(searches)

# Finds the searchResults for 4 words at a time
# Calls findSearches
def findSearchResults(array):
    fourWordsArray = array[:4]
    findSearches(fourWordsArray)

    for search in searches:
        temp = []
        results = spotify.search(q='track:' + search, type='track') # do the search
        index = len(results['tracks']['items']) # index = number of search results

        # for search, add the name of the song into the temp array.
        for x in range(index):
            name = results['tracks']['items'][x]['album']['name']
            temp.append(name)

        potentialSongs.append(temp)

    #print(searches)
    #print("Printing Potential Songs")
    #print(potentialSongs)

# Remove brackets from a list of songs
def removeFromList(songs):
    i = 0
    for song in songs:
        split = song.split("(")
        altered_song = split[0]
        songs[i] = altered_song
        i += 1

# Remove brackets from all songs in potential songs list
def removeFromAll(songsList):
    for songs in songsList:
        i = 0
        potentialSongs[i] = removeFromList(songs)
        i += 1

def main():
    findSearchResults(words)
    print()
    print(potentialSongs)
    removeFromAll(potentialSongs)
    print()
    print("Printing potential songs without brackets")
    print()
    print(potentialSongs)

main()


'''
def findClosestPlaylist():
    # picks the playlist that most accurately matches the description

    if len(sys.argv) > 1:
        name = ' '.join(sys.argv[1:])
    else:
        name = 'Radiohead'
'''
