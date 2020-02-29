import random
import spotipy
import datetime
import pytz

from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import oauth2
from spotify import secrets
from .forms import UsernameForm

from . import utils
from . import request as rq
from . import db
from django.core.exceptions import ObjectDoesNotExist
import requests
import base64
import json


redirect_uri = 'http://localhost:8000/callback/'
scope = 'user-library-read user-read-currently-playing user-top-read user-read-recently-played playlist-modify-public'
username = ""

def index(request):
    return render(request, 'playback/index.html', {})

def favorites(request):
    return render(request, 'playback/favorites.html', {})

def graph(request):
    return render(request, 'playback/graph.html', {'values': [['foo', 32], ['bar', 64], ['baz', 96]]})

def auth(request):
    auth_url = "https://accounts.spotify.com/authorize?response_type=token&client_id=" + secrets.CLIENT_ID + "&scope=" + utils.encodeURIComponent(scope) + "&redirect_uri=" + redirect_uri
    return HttpResponseRedirect(auth_url)

def auth_test(request):
    auth_url = "https://accounts.spotify.com/authorize?response_type=code&client_id=" + secrets.CLIENT_ID + "&scope=" + utils.encodeURIComponent(scope) + "&redirect_uri=" + "http://localhost:8000/add_test/"
    return HttpResponseRedirect(auth_url)

def add_test(request):
    auth_str = '{}:{}'.format(secrets.CLIENT_ID, secrets.CLIENT_SECRET)
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    auth_token = request.GET.get('code')
    code_payload = {
		'grant_type': 'authorization_code',
		'code': str(auth_token),
		'redirect_uri': "http://localhost:8000/add_test/",
	}

    auth_str = '{}:{}'.format(secrets.CLIENT_ID, secrets.CLIENT_SECRET)
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    headers = {
		'Content-Type': 'application/x-www-form-urlencoded',
		'Authorization': 'Basic {}'.format(b64_auth_str)
	}

    post_request = requests.post('https://accounts.spotify.com/api/token', data=code_payload, headers=headers)

    response_data = json.loads(post_request.text)

    refresh_token = response_data['refresh_token']

    refresh_payload = {
        'grant_type': 'refresh_token',
        'refresh_token': response_data['refresh_token']
    }

    post_refresh = requests.post('https://accounts.spotify.com/api/token', data=refresh_payload, headers=headers)
    return HttpResponse(str(json.loads(post_refresh.text)))

def callback(request):
    params = request.GET.urlencode().split('&')
    if params == ['']:
        return render(request, 'playback/fuckinghash.html', {})
    access_token = params[0].split('=')[1]
    db.new_user("yeet",datetime.datetime.now(pytz.timezone('Europe/London')),access_token)
    user = db.get_user(access_token)
    if not params[0]:
        return HttpResponse("No clue what happend. Code: 500")
    else:
        if len(params) == 1:
            res = rq.top_artists(access_token)
        elif len(params) == 2:
            res = rq.top_artists(access_token, params[1].split("=")[1])
        elif len(params) == 3:
            mode_type = params[2].split("=")[1]
            mode = params[1].split("=")[1]
            if (mode_type == "artist" and mode in {"long_term", "medium_term", "short_term"}):
                res = rq.top_artists(access_token,mode)
            elif (mode_type == "track" and mode in {"long_term", "medium_term", "short_term"}):
                res = rq.top_tracks(access_token,mode)
                return render(request, 'playback/favorites_track.html',{'results': res})
            elif (mode_type == "graph" and mode in {"long_term", "medium_term", "short_term"}):
                res = rq.top_artists(access_token,mode)
                return render(request, 'playback/graph.html', {'values':utils.parse_result_artist(user, res, mode)})
            else:
                res = [{"ERROR":{"Error":"An error occured"}}]
        else:
            res = [{"ERROR":{"Error":"An error occured"}}]
    return render(request, 'playback/favorites_artist.html',{'results': res})

def playback(request):
    token = request.GET.urlencode().split('&')[0].split('=')[1]
    devices = rq.playback_get_devices(token)
    playback = rq.playback_get_current_playback(token)
    rq.playback_get_current_playback(token)

    yeet = rq.playlist_add(token, '2Mlyguyh81oqe0RDJ6mx19', ['spotify:track:1wVMkGi3vQlLSpO04RKzgm'])
    rq.print_json(yeet)
    return render(request, 'playback/playback.html', context={'devices':devices,'playback':playback})

def add_songs(request):
    yeet = rq.playlist_add(token, '2Mlyguyh81oqe0RDJ6mx19', ['spotify:track:1wVMkGi3vQlLSpO04RKzgm'])