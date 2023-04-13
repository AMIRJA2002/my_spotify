from django.contrib.auth import get_user_model

User = get_user_model()


def check_for_existing_user(value: str):
    if User.objects.filter(email=value).exists():
        print(True)
        return True
    print(False)
    return False


def get_user(email):
    return User.objects.get(email=email)