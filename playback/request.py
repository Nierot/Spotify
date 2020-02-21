import spotipy
import requests
from spotipy import oauth2
from spotipy.oauth2 import SpotifyClientCredentials
from spotify import secrets
from . import utils

def top_artists(token, range="long_term", amount=50):
    results = requests.get("https://api.spotify.com/v1/me/top/artists?limit=" + str(amount) + "&time_range=" + range, headers={'Authorization': "Bearer " + token}).json()
    res = []
    i = 1
    while i < amount + 1:
        res.append({
            results['items'][i - 1]['name']:{                             # artist
                results['items'][i - 1]['images'][2]['url']:              # icon
                results['items'][i-1]['genres']                           # genres //TODO count which one is most popular
            }
        })
        i += 1
    return res

def top_tracks(token, range = "long_term", amount = 50):
    results = requests.get("https://api.spotify.com/v1/me/top/tracks?limit=" + str(amount) + "&time_range=" + range, headers={'Authorization': "Bearer " + token}).json()
    res = []
    i = 1
    while i < amount + 1:
        res.append({
            results['items'][i - 1]['name']:{
                results['items'][i - 1]['album']['images'][1]['url']:
                results['items'][i - 1]['album']['artists'][0]['name']
            }
        })
        i += 1        
    return res