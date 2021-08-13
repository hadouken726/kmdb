from django.urls import path
from api.views import AccountView


urlpatterns = [
    path('accounts/', AccountView.as_view())
]