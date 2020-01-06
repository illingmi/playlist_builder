import requests
import spotipy
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
words = ['The', 'King', 'And', 'Queen', 'Had', '2', 'Daughters', 'Their', 'Names',
          'Were', 'Olivia', 'And', 'Emerald']

#print(json.dumps(name, sort_keys=True, indent=4))
searches = []
potentialSongs = []

def findSearchResults(array):
    for i in range(4):
        # if array of words is not empty --> need a different way to write this
        #if array:
        # Finds all the potential songs searches up to five words
        if i == 0:
            search = array[i]
            prevSearch = search
            searches.append(search)
        else:
            search = prevSearch + " " + array[i]
            prevSearch = search
            searches.append(search)

        # get search results
        temp = []
        results = spotify.search(q='track:' + search, type='track')
        index = len(results['tracks']['items'])
        for x in range(index):
            name = results['tracks']['items'][x]['album']['name']
            temp.append(name)

        potentialSongs.append(temp)
    print(searches)
    print(potentialSongs)

test = ['The', 'King', 'And', 'Queen']
findSearchResults(test)
print(potentialSongs[0][0])
#potentialSongs[0].find(searches[0])
print(searches[0])


#results1 = spotify.search(q='track:The King')
#print(results1)
test = []

results = spotify.search(q='track:The King', type='track')
#print(json.dumps(results, sort_keys=True, indent=4))

name1 = results['tracks']['items'][0]['album']['name']
name2 = results['tracks']['items'][1]['album']['name']
name3 = results['tracks']['items'][2]['album']['name']
name4 = results['tracks']['items'][3]['album']['name']
name5 = results['tracks']['items'][4]['album']['name']
name6 = results['tracks']['items'][5]['album']['name']
name7 = results['tracks']['items'][6]['album']['name']
name8 = results['tracks']['items'][7]['album']['name']
none = results['tracks']['items'][9]['album']['name']

test.append([name1, name2, name3, name4, name5, name6, name7, name8])
#print("Hard Coded:")
#print(test)



'''
def findClosestPlaylist():
    # picks the playlist that most accurately matches the description

    if len(sys.argv) > 1:
        name = ' '.join(sys.argv[1:])
    else:
        name = 'Radiohead'
'''
