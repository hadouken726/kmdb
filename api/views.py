from django.contrib.auth.models import User
from django.db.models import fields
from rest_framework import mixins, request
from rest_framework.permissions import AllowAny
from api.models import Movie, Review
from rest_framework.views import APIView, Response, status
from api.serializers import AccountSerializer, LoginSerializer, MovieDetailSerializer, MovieSerializer, ReviewSerializer
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveDestroyAPIView, get_object_or_404
from rest_framework.authentication import TokenAuthentication
from api.permissions import IsAdmin, Any, IsCritic
from django.db.utils import IntegrityError


class AccountView(APIView):
    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except IntegrityError:
            return Response(data={'msg': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

class MovieView(ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin | Any]

    def list(self, request, *args, **kwargs):
        if request.data:
            deserializer = self.get_serializer(data=request.data, fields=('title',))
            deserializer.is_valid(raise_exception=True)
            serializer = self.get_serializer(instance=Movie.objects.filter(title__icontains=deserializer.validated_data['title']), fields=('id', 'title', 'duration', 'genres', 'premiere', 'classification', 'synopsis'), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return super().list(request, *args, **kwargs)


class MovieDetailView(RetrieveDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin | Any]


    def get(self, request, *args, **kwargs):
        if isinstance(request.user, User):
            serializer = self.get_serializer(self.get_object(), fields=('id', 'title', 'duration', 'genres', 'premiere', 'classification', 'synopsis', 'reviews'))
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(self.get_object(), fields=('id', 'title', 'duration', 'genres', 'premiere', 'classification', 'synopsis'))
        return Response(serializer.data, status=status.HTTP_200_OK)  


class ReviewView(mixins.UpdateModelMixin, mixins.CreateModelMixin, mixins.ListModelMixin, GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin | IsCritic]
    lookup_field = 'movie_id'
    
    
    def get_queryset(self):
        if self.request.method == 'GET':
            if not self.request.user.is_superuser:
                return Review.objects.filter(critic=self.request.user)
            return Review.objects.all()
        if self.request.method == 'PUT':
            return Review.objects.filter(critic=self.request.user, movie__id=self.kwargs['movie_id'])


    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ReviewSerializer(queryset, fields=('id', 'critic', 'stars', 'review', 'spoilers', 'movie'), many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    

    def post(self, request, *args, **kwargs):
        deserializer = ReviewSerializer(data=self.request.data, fields=('stars', 'review', 'spoilers'))
        deserializer.is_valid(raise_exception=True)
        movie = get_object_or_404(Movie.objects.all(), id=self.kwargs['movie_id'])
        if Review.objects.filter(movie__id=movie.id, critic=self.request.user).first():
            return Response(data={"detail": "You already made this review."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        review = Review.objects.create(critic=self.request.user, movie=movie, **deserializer.validated_data)
        serializer = ReviewSerializer(instance=review)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


