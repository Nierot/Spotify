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


redirect_uri = 'http://spotify.nierot.com/callback/'
scope = 'user-library-read user-read-currently-playing user-top-read user-read-recently-played'
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