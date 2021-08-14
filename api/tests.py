from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
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
        cls.critic = User.objects.create(
            **{
                "username": "Carioca",
                "password": "1234",
                "first_name": "Zé",
                "last_name": "Carioca",
                "is_superuser": False,
                "is_staff": True
            } 
        )
        cls.stars = 10
        cls.review = "erer erfoer ferf erferfy erfeyhf8eyf8eyfh9e8f efy ..."
        cls.spoilers = False
        cls.review_instance = Review.objects.create(
            movie=cls.movie,
            critic=cls.critic, 
            stars=cls.stars,
            review=cls.review,
            spoilers =cls.spoilers
        )
    

    def test_create_movie_success(self):
        self.assertIsNotNone(self.review_instance.id)


class AccountViewTest(TestCase):
    
    @classmethod
    def setUpTestData(cls) -> None:
        cls.client = APIClient()
        cls.route = '/api/accounts/'
        cls.user_data = {
            "username": "user",
            "password": "1234",
            "first_name": "John",
            "last_name": "Wick",
            "is_superuser": False,
            "is_staff": False
        }
        
    
    def test_user_successfullly_created(self):
        response = self.client.post(self.route, self.user_data, format='json')
        expected_response_data = {
            "id": 1,
            "username": "user",
            "first_name": "John",
            "last_name": "Wick",
            "is_superuser": False,
            "is_staff": False
        }
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_response_data)


    def test_user_already_exists(self):
        User.objects.create(**self.user_data)
        getted_user = User.objects.filter(username=self.user_data['username']).first()
        self.assertIsNotNone(getted_user)
        response = self.client.post(self.route, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'username': ["A user with that username already exists."]})


class LoginViewTest(TestCase):
    
    @classmethod
    def setUpTestData(cls) -> None:
        cls.client = APIClient()
        cls.login_data = {'username': 'John', 'password': '123456'}
        cls.user_data = {
            "username": "John",
            "password": "123456",
            "first_name": "John",
            "last_name": "Wick",
            "is_superuser": False,
            "is_staff": True
        }
    
    def test_user_successfully_logged(self):
        user_data = self.user_data.copy()
        user_data['password'] = make_password(user_data['password'])
        user = User.objects.create(**self.user_data)
        token = Token.objects.create(user=user).key
        response = self.client.post('/api/login/', self.login_data, format='json')
        self.assertEqual(response.data, {'token': token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)




        



