import spotipy
import requests
import json
from spotipy import oauth2
from spotipy.oauth2 import SpotifyClientCredentials
from spotify import secrets
from . import utils

API_LINK = "https://api.spotify.com"
# print(json.dumps(results, indent=2))

def do_get(token, endpoint):
    return requests.get(API_LINK + endpoint, headers={'Authorization': 'Bearer ' + token}).json()

def do_post(token, endpoint):
    return requests.post(API_LINK + endpoint, headers={'Authorization': 'Bearer ' + token}).json()

def do_put(token, endpoint):
    return requests.put(API_LINK + endpoint, headers={'Authorization': 'Bearer ' + token}).json()

def print_json(j):
    print(json.dumps(j, indent=2))

def top_artists(token, range="long_term", amount=50):
    results = do_get(token, "/v1/me/top/artists" + "?limit=" + str(amount) + "&time_range=" + range)
    res = []
    i = 1
    while i < amount + 1:
        res.append({
            results['items'][i - 1]['name']:{                             # artist
                results['items'][i - 1]['images'][1]['url']:              # icon
                results['items'][i - 1]['genres']                           # genres //TODO count which one is most popular
            }
        })
        i += 1
    return res

def top_tracks(token, range = "long_term", amount = 50):
    results = do_get(token, "/v1/me/top/tracks" +"?limit=" + str(amount) + "&time_range=" + range)
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

def playback_get_devices(token):
    results = do_get(token, "/v1/me/player/devices")
    res = []
    for device in results['devices']:
        res.append({
            "name":device['name'],
            "id":device['id'],
        })
    return res


def playback_pause(token):
    results = do_put(token, "/v1/me/player/pause")

def playback_volume(token, volume):
    return "nee"

def playback_previous(token):
    return ""

def playback_next(token):
    return ""

def playback_get_current_playback(token):
    results = do_get(token, "/v1/me/player")

    artists = []
    for artist in results['item']['album']['artists']:
        artists.append(artist['name'])

    device = results['device']['name']

    progress = utils.ms_to_minutes_and_seconds(results['progress_ms'])

    duration = utils.ms_to_minutes_and_seconds(results['item']['duration_ms'])

    cover = results['item']['album']['images'][1]['url']

    track_name = results['item']['name']

    is_playing = results['is_playing']
    return {'artists': artists,
            'device': device,
            'progress': progress,
            'duration': duration,
            'cover': cover,
            'track_name': track_name,
            'is_playing': is_playing,
            }

def playlist_add(token, playlist, songs):
    return do_post(token,"/v1/playlists/" + playlist + "/tracks?uris=" + ','.join(songs))
