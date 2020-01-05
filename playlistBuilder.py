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

# USER ID: mibaeoch3ierdvfq3g2wdvvl5
# PLAYLIST ID: <your playlist id>

# USER AUTHENTICATION COMMANDS:
    # $env:SPOTIPY_CLIENT_ID="26fd947cd19549f0a90ecaed2aab905d"
    # $env:SPOTIPY_CLIENT_SECRET="46402d169e204898a6f7cb6883bffd73"
    # $env:SPOTIPY_REDIRECT_URI="http://google.ca/"

# Erase cache and prompt for user permission
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

# Finds all the potential songs searches up to five words
def findPotentialSearches():
    # if array of words is not empty
    if words:
        search1 = words[0]
        search2 = words[0] + " " + words[1]
        search3 = words[0] + " " + words[1] + " " + words[2]
        search4 = words[0] + " " + words[1] + " " + words[2] + " " + words[3]
        search5 = words[0] + " " + words[1] + " " + words[2] + " " + words[3] + " " + words[4]

def findPotentialSongs():
    potentials1 = []
    potentials2 = []
    potentials3 = []
    potentials4 = []
    potentials5 = []
    #for (i = 1; i <= 5; i++)
    results1 = spotify.search(q='track:' + search1)

    '''first = results1['tracks']['items'][0]['album']['name']
    sec = results1['tracks']['items'][1]['album']['name']
    third = results1['tracks']['items'][2]['album']['name']
    forth = results1['tracks']['items'][3]['album']['name']


    #print(json.dumps(name, sort_keys=True, indent=4))
    potentials1.extend([name1, name2, name3, name4])
    print(potentials1)
    '''

if words:
    search1 = words[0]
    search2 = words[0] + " " + words[1]
    search3 = words[0] + " " + words[1] + " " + words[2]
    search4 = words[0] + " " + words[1] + " " + words[2] + " " + words[3]
    search5 = words[0] + " " + words[1] + " " + words[2] + " " + words[3] + " " + words[4]

print(search1)
print(search2)
print(search3)
print(search4)
print(search5)
print(words)

i = 1
results + str(1)

def findClosestPlaylist():
    # picks the playlist that most accurately matches the description

    if len(sys.argv) > 1:
        name = ' '.join(sys.argv[1:])
    else:
        name = 'Radiohead'
