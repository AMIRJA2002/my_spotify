from django.contrib.auth import get_user_model
from spotify_app.users.models import Profile

User = get_user_model()


def create_profile(name, user):
    Profile.objects.create(name=name, user=user)


def create_new_user(data):
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    user = User.objects.create_user(email=email, password=password)
    create_profile(name, user)
    return user
