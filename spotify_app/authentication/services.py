from django.contrib.auth import get_user_model
from spotify_app.users.models import Profile
User = get_user_model()


def create_new_user(data):
    email = data.get('email')
    password = data.get('password')
    return User.objects.create_user(email=email, password=password)


def create_profile(data, user):
    name = data.get('name')
    Profile.objects.create(name=name, user=user)
