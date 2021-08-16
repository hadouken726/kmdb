from api.models import Movie
from rest_framework.views import APIView, Response, status
from api.serializers import AccountSerializer, LoginSerializer, MovieSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.authentication import TokenAuthentication
from api.permissions import IsAdmin


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


class MovieView(CreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]


