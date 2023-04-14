from django.contrib.auth import get_user_model

User = get_user_model()


def check_for_existing_user(value: str):
    if User.objects.filter(email=value).exists():
        return True
    return False


def get_user(email):
    return User.objects.get(email=email)
