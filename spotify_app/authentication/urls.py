from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.UserSignUpApi.as_view(), name='signup'),
    path('login/', views.UserLoginApi.as_view(), name='login'),
]
