from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User, UserManager
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from api.models import Movie, Genre, Review
import json


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
        user = User.objects.create(**user_data)
        token = Token.objects.create(user=user).key
        response = self.client.post('/api/login/', self.login_data, format='json')
        self.assertEqual(response.data, {'token': token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MovieViewTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.admin_user_data = {
            "username": "John",
            "password": "123456",
            "first_name": "John",
            "last_name": "Wick",
            "is_superuser": True,
            "is_staff": True
        }
        cls.critic_user_data = {
            "username": "Jack",
            "password": "123456",
            "first_name": "Jack",
            "last_name": "Mars",
            "is_superuser": False,
            "is_staff": True
        }
        cls.route = '/api/movies/'
        cls.success_movie_data = {
            "title": "O Poderoso Chefão 2",
            "duration": "175m",
            "genres": [
                {"name": "Crime"},
                {"name": "Drama"}
            ],
            "premiere": "1972-09-10",
            "classification": 14,
            "synopsis": "Don Vito Corleone (Marlon Brando) é o chefe de uma ..."
        }
        cls.repeated_genre_movie_data = {
            "title": "O Poderoso Chefão 2",
            "duration": "175m",
            "genres": [
                {"name": "Crime"},
                {"name": "criMe"}
            ],
            "premiere": "1972-09-10",
            "classification": 14,
            "synopsis": "Don Vito Corleone (Marlon Brando) é o chefe de uma ..."
        }
        cls.movies_data_to_test_get_method = [
            {
            "title": "O Poderoso Chefão 2",
            "duration": "175m",
            "genres": [
                {"name": "Crime"},
                {"name": "Drama"}
            ],
            "premiere": "1972-09-10",
            "classification": 14,
            "synopsis": "Don Vito Corleone (Marlon Brando) é o chefe de uma ..."
            },
            {
            "title": "John Wick",
            "duration": "144m",
            "genres": [
                {"name": "Ação"}
            ],
            "premiere": "2014-09-23",
            "classification": 16,
            "synopsis": "Continental ..."
            }
        
        ]

    def test_admin_can_create_movie(self):
        client = APIClient()
        password = make_password(self.admin_user_data.pop('password'))
        admin_user = User.objects.create(**self.admin_user_data, password=password)
        token = Token.objects.create(user=admin_user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.post(self.route, self.success_movie_data, format='json')
        created_movie = Movie.objects.filter(id=1).first()
        self.assertIsNotNone(created_movie)
        expected_response = {
            "id": 1,
            "title": "O Poderoso Chefão 2",
            "duration": "175m",
            "genres": [
                {
                    "id": 1,
                    "name": "Crime"
                },
                {
                    "id": 2,
                    "name": "Drama"
                }
            ],
            "premiere": "1972-09-10",
            "classification": 14,
            "synopsis": "Don Vito Corleone (Marlon Brando) é o chefe de uma ..."
        }
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_response)


    def test_can_not_create_repeated_movie_genre(self):
        client = APIClient()
        password = make_password(self.admin_user_data.pop('password'))
        admin_user = User.objects.create(**self.admin_user_data, password=password)
        token = Token.objects.create(user=admin_user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.post(self.route, self.repeated_genre_movie_data, format='json')
        created_movie = Movie.objects.filter(id=1).first()
        self.assertIsNotNone(created_movie)
        self.assertEqual(created_movie.genres.count(), 1)
        self.assertEqual(created_movie.genres.first().id, 1)
        expected_response = {
            "id": 1,
            "title": "O Poderoso Chefão 2",
            "duration": "175m",
            "genres": [
                {
                    "id": 1,
                    "name": "Crime"
                }
            ],
            "premiere": "1972-09-10",
            "classification": 14,
            "synopsis": "Don Vito Corleone (Marlon Brando) é o chefe de uma ..."
        }
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_response)
    

    def test_anonymous_user_can_get_movies(self):
        genres_set = [movie.pop('genres') for movie in self.movies_data_to_test_get_method]
        for i, movie_data in enumerate(self.movies_data_to_test_get_method):
            movie = Movie.objects.create(**movie_data)
            genres = [Genre.objects.create(**genre) for genre in genres_set[i]]
            movie.genres.set(genres)
        client = APIClient()
        response = client.get(self.route)
        expected_data = [
            {
            "id": 1,
            "title": "O Poderoso Chefão 2",
            "duration": "175m",
            "genres": [
                {"id": 1, "name": "Crime"},
                {"id": 2, "name": "Drama"}
            ],
            "premiere": "1972-09-10",
            "classification": 14,
            "synopsis": "Don Vito Corleone (Marlon Brando) é o chefe de uma ..."
            },
            {
            "id": 2,
            "title": "John Wick",
            "duration": "144m",
            "genres": [
                {"id": 3, "name": "Ação"}
            ],
            "premiere": "2014-09-23",
            "classification": 16,
            "synopsis": "Continental ..."
            }
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
    
    def test_critic_can_get_movies(self):
        genres_set = [movie.pop('genres') for movie in self.movies_data_to_test_get_method]
        for i, movie_data in enumerate(self.movies_data_to_test_get_method):
            movie = Movie.objects.create(**movie_data)
            genres = [Genre.objects.create(**genre) for genre in genres_set[i]]
            movie.genres.set(genres)
        client = APIClient()
        password = make_password(self.critic_user_data.pop('password'))
        critic_user = User.objects.create(**self.critic_user_data, password=password)
        token = Token.objects.create(user=critic_user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(self.route)
        expected_data = [
            {
            "id": 1,
            "title": "O Poderoso Chefão 2",
            "duration": "175m",
            "genres": [
                {"id": 1, "name": "Crime"},
                {"id": 2, "name": "Drama"}
            ],
            "premiere": "1972-09-10",
            "classification": 14,
            "synopsis": "Don Vito Corleone (Marlon Brando) é o chefe de uma ..."
            },
            {
            "id": 2,
            "title": "John Wick",
            "duration": "144m",
            "genres": [
                {"id": 3, "name": "Ação"}
            ],
            "premiere": "2014-09-23",
            "classification": 16,
            "synopsis": "Continental ..."
            }
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
    

    def test_admin_can_get_movies(self):
        genres_set = [movie.pop('genres') for movie in self.movies_data_to_test_get_method]
        for i, movie_data in enumerate(self.movies_data_to_test_get_method):
            movie = Movie.objects.create(**movie_data)
            genres = [Genre.objects.create(**genre) for genre in genres_set[i]]
            movie.genres.set(genres)
        client = APIClient()
        password = make_password(self.admin_user_data.pop('password'))
        admin_user = User.objects.create(**self.admin_user_data, password=password)
        token = Token.objects.create(user=admin_user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(self.route)
        expected_data = [
            {
            "id": 1,
            "title": "O Poderoso Chefão 2",
            "duration": "175m",
            "genres": [
                {"id": 1, "name": "Crime"},
                {"id": 2, "name": "Drama"}
            ],
            "premiere": "1972-09-10",
            "classification": 14,
            "synopsis": "Don Vito Corleone (Marlon Brando) é o chefe de uma ..."
            },
            {
            "id": 2,
            "title": "John Wick",
            "duration": "144m",
            "genres": [
                {"id": 3, "name": "Ação"}
            ],
            "premiere": "2014-09-23",
            "classification": 16,
            "synopsis": "Continental ..."
            }
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)


class MovieDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.admin_user_data = {
            "username": "John",
            "first_name": "John",
            "last_name": "Wick",
            "is_superuser": True,
            "is_staff": True
        }
        cls.critic_user_data = {
            "username": "Jack",
            "first_name": "Jack",
            "last_name": "Mars",
            "is_superuser": False,
            "is_staff": True
        }
        cls.review_data = {
            "stars": 7,
            "review": "O Poderoso Chefão 2 podia ter dado muito errado...",
            "spoilers": False
        }
        cls.movie_data = {
            "title": "O Poderoso Chefão 2",
            "duration": "175m",
            "genres": [
                {"name": "Crime"},
                {"name": "Drama"}
            ],
            "premiere": "1972-09-10",
            "classification": 14,
            "synopsis": "Don Vito Corleone (Marlon Brando) é o chefe de uma ..."
        }
    

    def test_movie_getted_by_admin_user(self):
        admin_user = User.objects.create(**self.admin_user_data)
        admin_user.set_password('123456')
        critic_user = User.objects.create(**self.critic_user_data)
        critic_user.set_password('123456')
        token = Token.objects.create(user=admin_user)
        genres_data = self.movie_data.pop('genres')
        movie = Movie.objects.create(**self.movie_data)
        [movie.genres.add(Genre.objects.create(**genre)) for genre in genres_data]
        Review.objects.create(movie=movie, critic=critic_user, **self.review_data)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        response = client.get('/api/movies/1')
        expected_response = {
            "id": 1,
            "title": "O Poderoso Chefão 2",
            "duration": "175m",
            "genres": [
                {"id": 1, "name": "Crime"},
                {"id": 2, "name": "Drama"}
            ],
            "premiere": "1972-09-10",
            "classification": 14,
            "synopsis": "Don Vito Corleone (Marlon Brando) é o chefe de uma ...",
            "reviews": [
                {
                "id": 1,
                "critic": {
                    "id": 2,
                    "first_name": "Jack",
                    "last_name": "Mars"
                    },
                "stars": 7,
                "review": "O Poderoso Chefão 2 podia ter dado muito errado...",
                "spoilers": False
                }
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)
    

    def test_movie_getted_by_critic_user(self):
        critic_user = User.objects.create(**self.critic_user_data)
        critic_user.set_password('123456')
        token = Token.objects.create(user=critic_user)
        genres_data = self.movie_data.pop('genres')
        movie = Movie.objects.create(**self.movie_data)
        [movie.genres.add(Genre.objects.create(**genre)) for genre in genres_data]
        Review.objects.create(movie=movie, critic=critic_user, **self.review_data)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        response = client.get('/api/movies/1/')
        expected_response = {
            "id": 1,
            "title": "O Poderoso Chefão 2",
            "duration": "175m",
            "genres": [
                {"id": 1, "name": "Crime"},
                {"id": 2, "name": "Drama"}
            ],
            "premiere": "1972-09-10",
            "classification": 14,
            "synopsis": "Don Vito Corleone (Marlon Brando) é o chefe de uma ...",
            "reviews": [
                {
                "id": 1,
                "critic": {
                    "id": 2,
                    "first_name": "Jack",
                    "last_name": "Mars"
                    },
                "stars": 7,
                "review": "O Poderoso Chefão 2 podia ter dado muito errado...",
                "spoilers": False
                }
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)
    

    def test_movie_getted_by_anonymous_user(self):
        critic_user = User.objects.create(**self.critic_user_data)
        critic_user.set_password('123456')
        genres_data = self.movie_data.pop('genres')
        movie = Movie.objects.create(**self.movie_data)
        [movie.genres.add(Genre.objects.create(**genre)) for genre in genres_data]
        Review.objects.create(movie=movie, critic=critic_user, **self.review_data)
        client = APIClient()
        response = client.get('/api/movies/1/')
        expected_response = {
            "id": 1,
            "title": "O Poderoso Chefão 2",
            "duration": "175m",
            "genres": [
                {"id": 1, "name": "Crime"},
                {"id": 2, "name": "Drama"}
            ],
            "premiere": "1972-09-10",
            "classification": 14,
            "synopsis": "Don Vito Corleone (Marlon Brando) é o chefe de uma ..."
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    
    def test_invalid_movie_id_from_url(self):
        client = APIClient()
        response = client.get('/api/movies/1/')
        self.assertEqual(response.data, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'detail': 'Not found.'})
    

    def test_delete_movie_by_admin(self):
        admin_user = User.objects.create(**self.admin_user_data)
        admin_user.set_password('123456')
        critic_user = User.objects.create(**self.critic_user_data)
        critic_user.set_password('123456')
        token = Token.objects.create(user=admin_user)
        genres_data = self.movie_data.pop('genres')
        movie = Movie.objects.create(**self.movie_data)
        [movie.genres.add(Genre.objects.create(**genre)) for genre in genres_data]
        Review.objects.create(movie=movie, critic=critic_user, **self.review_data)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        response = client.delete('/api/movies/1/')
        self.assertIsNone(Review.objects.filter(id=1).first())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, '')
    

    def test_critic_user_try_delete_movie(self):
        critic_user = User.objects.create(**self.critic_user_data)
        critic_user.set_password('123456')
        token = Token.objects.create(user=critic_user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        response = client.delete('/api/movies/1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    

    def test_anonymous_user_try_delete_movie(self):
        client = APIClient()
        response = client.delete('/api/movies/1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)