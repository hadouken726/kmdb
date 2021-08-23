from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from api.models import Movie
from rest_framework.views import APIView, Response, status
from api.serializers import AccountSerializer, LoginSerializer, MovieDetailSerializer, MovieSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.authentication import TokenAuthentication
from api.permissions import IsAdmin, Any


class AccountView(APIView):
    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)


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