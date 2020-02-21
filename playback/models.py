from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Artist(models.Model):
    name = models.CharField(max_length=200)
    genres = models.ManyToManyField(Genre)
    def __str__(self):
        return self.name
    
class Track(models.Model):
    name = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre)
    def __str__(self):
        return self.name

class User(models.Model):
    name = models.CharField(primary_key=True, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=500,default=None, blank=True, null=True)
    def __str__(self):
        return self.token

class Liked_track(models.Model):
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    term = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.track.name

class Liked_artist(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    term = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.artist.name

class Liked_genre(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    term = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.genre.name