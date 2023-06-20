from django.urls import path
from . import apis


urlpatterns = [
    path('signup/', apis.UserSignUpApi.as_view(), name='signup'),
    path('login/', apis.UserLoginApi.as_view(), name='login'),
    path('artists/', apis.Artist.as_view(), name='artists'),
]
