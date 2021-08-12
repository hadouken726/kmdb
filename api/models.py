from django.contrib.auth.models import User
from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=255)
    duration = models.CharField(max_length=255)
    premiere = models.DateField()
    classification = models.IntegerField()
    synopsis = models.TextField()


class Genre(models.Model):
    name = models.CharField(max_length=255)
    movies = models.ManyToManyField(Movie, related_name='genres')


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    stars = models.IntegerField()
    review = models.TextField()
    spoilers = models.BooleanField(default=False)
    critic = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
