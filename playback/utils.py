from . import db
from django.core.exceptions import ObjectDoesNotExist
from collections import Counter
from django.http import HttpResponse
import math
from playback.genre_seeds import GENRE_SEEDS

def list_to_string(list):
    res = ""
    for x in list:
        if res == "":
            res = x
        else:
            res = res + ", " + x
    return res

def parse_result_artist(user, res, term):
    artists = check_new_genres_artists(res)
    genres = get_genres(artists) #sorted(Counter(get_genres(artists)).items(), key=lambda x: x[1], reverse=True)
    res = []
    print(genres)
    i = 1
    for genre in genres:
        if genre.__str__() in GENRE_SEEDS['genres']:
            res.append(genre.__str__())
    res = Counter(res)
    print(res)

    return [['a',1]]
    # for pair in genres:
    #     if pair[1] <= 0:
    #         continue
    #     else:
    #         if pair[0].__str__() in GENRE_SEEDS['genres']:
    #             print(pair[0])
    #         foo = [pair[0], pair[1]]
    #         res.append(foo)
    # return res[:5]

    # TODO Add all artists to Liked_artists with term and user
    # TODO Add all genres from those artists to Liked_genres with term user

def get_genres(artists):
    res = []
    for a in artists:
        for genre in a.genres.all():
            res.append(genre)
    return res

def check_new_genres_artists(res):
    artists = []
    genres = []
    for x in res:
        artist_name = [*x][0]
        genres = x.get(artist_name).get([*x.get(artist_name)][0])
        try:
            artist = db.get_artist(artist_name)
        except ObjectDoesNotExist:
            genres_obj_list = []
            for y in genres:
                try:
                    genre = db.get_genre(y)
                except ObjectDoesNotExist:
                    genre = db.new_genre(y)
                genres_obj_list.append(genre)
                genres.append(genre)
            artist = db.new_artist(artist_name,genres_obj_list)
        artists.append(artist)
    return artists

def encodeURIComponent(comp):
    res = ''
    for letter in comp:
        if letter == " ":
            res = res + "%20"
        else:
            res = res + letter
    return res

def ms_to_minutes_and_seconds(ms):
    sec = ms/1000
    minute = 0
    while sec > 59:
        sec -= 60
        minute += 1
    return str(minute) + ":" + str(math.floor(sec))