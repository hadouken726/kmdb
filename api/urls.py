from django.urls import path
from api.views import AccountView, LoginView, MovieDetailView, MovieView


urlpatterns = [
    path('accounts/', AccountView.as_view()),
    path('login/', LoginView.as_view()),
    path('movies/', MovieView.as_view()),
    path('movies/<pk>/', MovieDetailView.as_view())
]