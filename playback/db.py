from . import models

def new_user(name, date, token):
    existing_users = models.User.objects.filter(token=token)
    if (len(models.User.objects.filter(token=token)) > 0):
        return False
    else:
        user = models.User(name=name,created_at=date,token=token)
        user.save()
        return True

def new_genre(name):
    genre = models.Genre(name=name)
    genre.save()
    return genre

def new_artist(name, genres):
    artist = models.Artist(name=name)
    artist.save()
    for genre in genres:
        artist.genres.add(genre)
    return artist

def new_track(name, artist):
    track = models.Track(name=name, artist=artist)
    track.save()
    return track

def add_liked_track(user, track, term):
    """
    Term is an integer, 1 for short_term, 2 for medium_term, and 3 for long_term 
    """
    liked_track = models.Liked_track(term=term, track=track, user=user)
    liked_track.save()
    return liked_track

def add_liked_artist(user, artist, term):
    """
    Term is an integer, 1 for short_term, 2 for medium_term, and 3 for long_term 
    """
    liked_artist = models.Liked_artist(term=term, artist=artist, user=user)
    liked_artist.save()
    return liked_artist

def add_liked_genre(user, genre, term):
    """
    Term is an integer, 1 for short_term, 2 for medium_term, and 3 for long_term 
    """
    liked_genre = models.Liked_genre(term=term, genre=genre, user=user)
    liked_genre.save()
    return liked_genre

def get_user(token):
    return models.User.objects.get(token=token)

def get_genre(name):
    return models.Genre.objects.get(name=name)

def get_artist(name):
    return models.Artist.objects.get(name=name)

def get_track(name):
    return models.Track.objects.get(name=name)

def add_genre_to_artist(genre,artist):
    artist.genres.add(genre)