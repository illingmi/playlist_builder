import requests
import spotipy
import os
import re
import sys
import json
import nltk.corpus
import spotipy.util as util
from json.decoder import JSONDecodeError
from nltk.corpus import stopwords

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
sw = stopwords.words("english")

#print(json.dumps(name, sort_keys=True, indent=4))

description1 = "Not me but my brother is a criminal defense attorney. He worked as a contracted public defender for a few years after starting his own business to get some guaranteed income while building his client base"
description2 = "During my days of insurance defense, I spent one lovely afternoon bickering with counsel for a co-defendant over who would be responsible for paying the $5000 that was keeping us from settling"
description3 = "Nothing sexual, sir. Just hard drugs and devil worship"
description4 = "Firm calls me in a panic, they need to redo the work on a tight deadline."
description5 = "Mom was a raging alcoholic that would bring random guys home many nights from the bar while the dad was working"
description6 = "On an unrelated note please continue to boil your drinking water due to pollution concerns"

f = open("potential_playlists.txt", "a+")

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
    songId = ''

# splits a search
def splitSearch(search):
    return search.split()

# removes brackets from a song
def removeBrackets(song):
    split = song.split("(")
    altered_song = split[0]
    return altered_song

# Returns an array of possible searches of up to 4 words
# ex: ['This', 'This is', 'This is my, 'This is my sentence']
def findSearches(words):
    searches = []
    i = 0
    fourWords = words[:4]
    print(fourWords)
    print("[3] findSearches")
    for word in fourWords:

        # gets the first one word search
        if i == 0:
            search = fourWords[i]
            prevSearch = search
            searches.append(search)

        # finds two, three and four word searches by combining the words together
        else:
            search = prevSearch + " " + fourWords[i]
            prevSearch = search
            searches.append(search)

        i += 1

    #print("Printing searches", searches)
    return searches

# Returns an array of all the songs that were generated from all of the four possible searches
# searches is an array of searches generated from findSearches
def findSongs(searches):
    #print("[4] findSongs")
    songs = []
    for search in searches:
        results = spotify.search(q='track:' + search, limit=50, type='track') # do the search
        index = len(results['tracks']['items']) # index = number of search results
        searchSplit = splitSearch(search)       # split the search keywords into an array
                                                # "the king" --> ['the', 'king']
                                                # this is used later to find the best song (findBestTitle())

        # for each song from the search, create a song, an add the corresponding search to the array
        for x in range(index):
            song = Song()
            name = results['tracks']['items'][x]['name']
            song.title = removeBrackets(name)
            song.search = search
            song.searchSplit = searchSplit
            song.songId = results['tracks']['items'][x]['id']
            songs.append(song)

    return songs



# find the songs that match exactly
# Stores matches in global 'exactMatches' array
def findExactMatches(songs):
    print("[6] findExactMatches")
    exactMatches = []

    for song in songs:
        title = song.title
        titleWords = title.split()
        numTitleChars = 0
        for word in titleWords:
            for c in word:
                numTitleChars +=1

        search = song.search
        searchWords = search.split()
        numSearchChars = 0
        for word in searchWords:
            for c in word:
                numSearchChars +=1

        # ignore upper/lowercase
        if re.search(search, title, re.IGNORECASE):
            if numSearchChars == numTitleChars:
                exactMatches.append(song)

        #print("Song title: ", title, "Tlength: ", tLength,"Associated Search: ", search, "searchLength: ", sLength)

    print("Printing Exact Matches: ")
    for song in exactMatches:
        print(song.title, song.searchSplit)

    return exactMatches

# Pick the song that corresponds to the longest search keyword (song at the last index of the array)
# Returns the best song
def chooseBestSong(bestSongs):
    print("[8] chooseBestSong")
    length = len(bestSongs)
    bestSong = bestSongs[length - 1]
    #finalSearch = finalSong.searchSplit
    print(bestSong.title)
    return bestSong

# Ranks all the songs and returns the songs with the highest rank
def findHighestRanked(songs):
    print("[7] findHighestRanked")
    highestRank = 0
    highestRankedSongs = []

    for song in songs:
        # FUTURE IDEA: if (search)word is not a stop word (in a list of stopwords),
        #              AND is in the song's title, increase song's rank by 2 pts, not 1
        searchToCompare = song.searchSplit
        for word in searchToCompare:
            if re.search(word, song.title, re.IGNORECASE):
                song.rank += 1
            if song.rank > highestRank:
                highestRank = song.rank

    #print("Songs Ranked:")
    for song in songs:
        #print(song.title, song.searchSplit, song.rank)
        if song.rank == highestRank:
            highestRankedSongs.append(song)

    '''
    print("Highest Ranked Songs:")
    for song in highestRankedSongs:
        print(song.title, song.searchSplit, song.rank)
    '''

    return highestRankedSongs

# Removes all the stopwords from a search and returns the new search
def removeStopWords(search):
    i = 0
    for word in search:
        if word in sw:
            search.pop(i)
        i += 1
    return search


# Used when stopwords have been removed from the search. For each song that
# was found with a search that does not contain stopwords, it makes sure that
# the song is correlated with the original search. This ensures that the correct
# number of words is removed the words array
def fixSongSearches(highestRanked, newSongs):
    orgSearch = highestRanked[0].search
    orgSearchSplit = highestRanked[0].searchSplit

    for song in newSongs:
        song.search = orgSearch
        song.searchSplit = orgSearchSplit

    return newSongs

# find the best song again
def findBestSong2(newSongs):
    exactMatches = findExactMatches(newSongs)
    highestRanked = findHighestRanked(newSongs)

    if exactMatches:
        bestSongs = exactMatches
        bestSong = chooseBestSong(bestSongs)

    else:
        bestSongs = highestRanked
        bestSong = bestSongs[0]

    return bestSong

def findEverythingAgain(currWords):
    newSearches = findSearches(currWords)
    newSongs = findSongs(newSearches)
    bestNewSongs = findExactMatches(newSongs)
    return bestNewSongs

# return the best song that mostly closely matches the search keywords.
# TODO: FIX - shouldn't need findBestSong2 if I'm flipping the firstTime Variable correctly
def findBestSong(words, songs):
    #print("[5] findBestSong")
    currWords = words[:4] # ["I" "love" "defense" "Lawyers"]
    print("Printing the current 4 words", currWords)
    exactMatches = findExactMatches(songs)
    highestRanked = findHighestRanked(songs)
    noMatch = True
    # if there are any song titles that are exact matches, choose the best song from exactMatches,
    # otherwise choose best song from highestRanked
    if exactMatches:
        bestSongs = exactMatches
        bestSong = chooseBestSong(bestSongs)
        return bestSong

    # if noMatch has been found yet
    elif noMatch:
         print("Inside findBestSong elif")
         print("Got into elif")
         currWords.pop(0)
         bestNewSongs = findEverythingAgain(currWords)
         if bestNewSongs:
             bestSong = chooseBestSong(bestNewSongs)
             noMatch = False
             return bestSong



    else:
        bestSongs = highestRanked
        bestSong = bestSongs[0]
        return bestSong

#bestSong = chooseBestSong(bestSongs)


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
#         find possible searches, find the search results, find the best song from the results and
#         add the best song to the finalSongs Array.
#         Then, pop any search words used from the words array
def findAllSongs(words):
    #print("[2] findAllSongs")
    finalSongs = []

    while words:
        searches = findSearches(words)
        songs = findSongs(searches)
        bestSong = findBestSong(words, songs)
        finalSongs.append(bestSong)
        popWords(bestSong, words)
        '''
        print("Print words after popped: ", words)
        print()
        for song in finalSongs:
            print(song.title)
        print()
        '''

    return finalSongs

# Given an array of finalSongs, adds each song to the playlist by their song id
def addSongsToPlaylist(finalSongs):
    # for song in finalSongs:
        # id = song.songid
        # playlist.addSong() (or however this is supposed to work)
    print("[10] addSongsToPlaylist")
    print("Added the final songs to the playlist!")

# write playlist to file
def writeSongsToFile(description, finalSongs):
    f.write("Description: ")
    f.write(description + "\n \n")
    f.write("Playlist: \n")
    for song in finalSongs:
        f.write(song.title + " \n")
    f.write("\n")

def runProgram(description):
    words = description.split() # create an array of single words
    #print("[1] Main: Split Description")
    # find all the titles and song ideas of all the songs that should be added into the playlist
    finalSongs = findAllSongs(words)

    #writeSongsToFile(description, finalSongs)
    addSongsToPlaylist(finalSongs)
    print("Printing Final Songs! ")
    for song in finalSongs:
        print(song.title)

    #print(json.dumps(results, sort_keys=True, indent=4))

#runProgram(description1)
