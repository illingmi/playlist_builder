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
#words = ['The', 'King', 'and', 'Queen', 'had', '2', 'daughters', 'Their', 'names',
          #'were', 'Olivia', 'and', 'Emerald']

#searches = []       # an array of search entries
#songs = []          # an array of songs objects
#exactMatches = []   # an array of titles that match exactly

# (string) title:       song title (does not include any words included inside brackets ())
# (string) search:      the corresponding search keywords that found this song title
# (array) searchSplit:  the corresponding search keywords parsed into an array of individual words
# (int) rank:           a number value that demonstrates how closely the title matches the search entry
# (string) songId:      the song id
class Song(object):
    title = ""
    search = ""
    searchSplit = []
    rank = 0
    songId = "no song id"

# splits a search
def splitSearch(search):
    return search.split()

# removes brackets from a song
def removeBrackets(song):
    split = song.split("(")
    altered_song = split[0]
    return altered_song

# get the four word search (to compare and rank the songs)
def getSearchToCompare(songs):
    length = len(songs)
    song = songs[length - 1]
    return song.searchSplit

# Returns an array of possible searches of up to 4 words
# ex: ['This', 'This is', 'This is my, 'This is my sentence']
def findSearches(words):
    searches = []
    #print("[3] findSearches")
    for i in range(4):

        # gets the first one word search
        if i == 0:
            search = words[i]
            prevSearch = search
            searches.append(search)

        # finds two, three and four word searches by combining the words together
        else:
            search = prevSearch + " " + words[i]
            prevSearch = search
            searches.append(search)

    #print(searches)
    return searches

# Returns an array of all the songs that were generated from all of the four possible searches
# searches is an array of searches generated from findSearches
def findSongs(searches):
    #print("[4] findSongs")
    songs = []
    for search in searches:
        results = spotify.search(q='track:' + search, type='track') # do the search
        index = len(results['tracks']['items']) # index = number of search results
        searchSplit = splitSearch(search)       # split the search keywords into an array
                                                # "the king" --> ['the', 'king']
                                                # this is used later to find the best song (findBestTitle())

        # for each song from the search, create a song, an add the corresponding search to the array
        for x in range(index):
            song = Song()
            name = results['tracks']['items'][x]['album']['name']
            song.title = removeBrackets(name)
            song.search = search
            song.searchSplit = searchSplit
            # song.songId = ...
            songs.append(song)


    #for song in songs:
        #print(song.title, "Search: ", song.search, "Search Split: ", song.searchSplit, song.rank)
    return songs

# find the songs that match exactly
# Stores matches in global 'exactMatches' array
def findExactMatches(songs):
    print("[6] findExactMatches")
    exactMatches = []

    for song in songs:
        title = song.title
        tLength = len(title.split())

        search = song.search
        sLength = len(search.split())

        if search in title and tLength == sLength:
            exactMatches.append(song)

    for song in exactMatches:
        print(song.title, "Search: ", song.search, "Search Split: ", song.searchSplit)
    return exactMatches

# Ranks all the songs and returns the songs with the highest rank
def findHighestRanked(songs):
    print("[7] findHighestRanked")
    highestRank = 0
    highestRankedSongs = []
    searchToCompare = getSearchToCompare(songs)
    for song in songs:
        # FUTURE IDEA: if (searcu)word is not a stop word (in a list of stopwords),
        #              AND is in the song's title, increase song's rank by 2 pts, not 1
        for word in searchToCompare:
            if word in song.title:
                song.rank += 1
            if song.rank > highestRank:
                highestRank = song.rank

    for song in songs:
        if song.rank == highestRank:
            highestRankedSongs.append(song)

    for song in highestRankedSongs:
        print(song.title, "Search: ", song.search, "Search Split: ", song.searchSplit, song.rank)

    return highestRankedSongs

# Pick the song that corresponds to the longest search keyword (song at the last index of the array)
# Returns the best song
def chooseBestSong(bestSongs):
    print("[8] chooseBestSong")
    length = len(bestSongs)
    bestSong = bestSongs[length - 1]
    #finalSearch = finalSong.searchSplit
    print(bestSong.title)
    return bestSong

# return the best song that mostly closely matches the search keywords.
def findBestSong(songs):
    #print("[5] findBestSong")
    exactMatches = findExactMatches(songs)
    highestRanked = findHighestRanked(songs)

    # if there are any song titles that are exact matches, choose the best song from exactMatches,
    # otherwise choose best song from highestRanked
    if exactMatches:
        bestSongs = exactMatches
        bestSong = chooseBestSong(bestSongs)
    else:
        bestSongs = highestRanked
        bestSong = bestSongs[0]

    #bestSong = chooseBestSong(bestSongs)
    return bestSong

# Pop the same number of words as the search result that produced the finalSong
def popWords(bestSong, words):
    print("[9] popWords")
    #print(words)
    numWordsToPop = len(bestSong.searchSplit)
    #print("Number of words to pop: ", numWordsToPop)
    i = 0
    while i < numWordsToPop:
        words.pop(0)
        #print(words)
        i += 1

# Returns an array of finalSongs --> all the songs that should be added into the final playlist
# Method: if there are still words from the description left to search:
#         find possible searhces, find the search results, find the best song from the results and
#         add the best song to the finalSongs Array.
#         Then, pop any search words used from the words array
def findAllSongs(words):
    #print("[2] findAllSongs")
    finalSongs = []

    while words:
        searches = findSearches(words)
        songs = findSongs(searches)
        bestSong = findBestSong(songs)
        finalSongs.append(bestSong)
        popWords(bestSong, words)
        print("Print words after popped: ", words)
        print()
        for song in finalSongs:
            print(song.title)
        print()

    return finalSongs

# Given an array of finalSongs, adds each song to the playlist by their song id
def addSongsToPlaylist(finalSongs):
    # for song in finalSongs:
        # id = song.songid
        # playlist.addSong() (or however this is supposed to work)
    print("[10] addSongsToPlaylist")
    print("Added the final songs to the playlist!")

def main():
    words = description.split() # create an array of single words
    #print("[1] Main: Split Description")
    # find all the titles and song ideas of all the songs that should be added into the playlist
    finalSongs = findAllSongs(words)
    addSongsToPlaylist(finalSongs)


    '''
    for song in songs:
        print(song.title, song.rank, song.search)
    finalSong = findBestTitle()
    for song in exactMatches:
        print(song.title, song.search)

    print("Add ", finalSong.title, " to the playlist!")
    '''

        #print("Title: ", song.title, "Search: ", song.search, "Search Split: ", song.searchSplit, song.rank)
    #findBestTitle()

main()

'''
temp = []
#currentSongs = potentialSongs[index] # the current song list that we're working with
i = 0
for search in searchesSplit:
    #term = search
    length = len(search)
    print(length)
    for word in search:
        print(word)

    if length == 1: # if the term has only one word
        print("One Term")
    else:
        print("Many Terms")

    i += 1

    # The song that will be added to the playlist. NEEDS some way to keep track of exactly which song this was
    # (string) title:       best song title (does not include any words included inside brackets ())
    # (array) searchSplit:  the corresponding search keywords parsed into an array of individual words
    class BestSong(object):
        title = ""
        searchSplit = []

'''
