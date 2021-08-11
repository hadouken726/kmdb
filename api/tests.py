from django.test import TestCase
from django.contrib.auth.models import User
from api.models import Movie, Genre, Review


class MovieModelTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.title = 'John Wick'
        cls.duration = '112m'
        cls.premiere = '2013-08-21'
        cls.classification = 16
        cls.synopsis = 'John Wick(Keanu Reeves) ...'
        cls.movie = Movie.objects.create(
            title=cls.title,
            duration=cls.duration,
            premiere=cls.premiere,
            classification=cls.classification,
            synopsis=cls.synopsis
        )
    

    def test_create_movie_success(self):
        self.assertIsNotNone(self.movie.id)


class GenreModelTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.name = 'Ação'
        cls.genre = Genre.objects.create(
            name=cls.name
        )
    

    def test_create_movie_success(self):
        self.assertIsNotNone(self.genre.id)


class ReviewModelTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.movie = Movie.objects.create(
            title='Titanic',
            duration='230m',
            premiere='2008-10-02',
            classification=14,
            synopsis='dewuhewe f3iugfb3f rfh3rfh'
        )
        cls.stars = 10
        cls.review = "erer erfoer ferf erferfy erfeyhf8eyf8eyfh9e8f efy ..."
        cls.spoilers = False
        cls.review_instance = Review.objects.create(
            movie=cls.movie, 
            stars=cls.stars,
            review=cls.review,
            spoilers =cls.spoilers
        )
    

    def test_create_movie_success(self):
        self.assertIsNotNone(self.review_instance.id)
    




