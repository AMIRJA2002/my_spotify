from .selectors import check_for_existing_user, get_user, get_all_artists
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from rest_framework import serializers, status
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from .services import create_new_user
from django.db import transaction

User = get_user_model()


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    tokens = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    return tokens


class UserSignUpApi(APIView):

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=200)
        email = serializers.EmailField()
        password = serializers.CharField()

        def validate_email(self, email):
            if check_for_existing_user(email):
                raise serializers.ValidationError("email already exist")
            return email

    @transaction.atomic()
    def post(self, reqeust):
        serializer = self.InputSerializer(data=reqeust.data)
        serializer.is_valid(raise_exception=True)
        new_user = create_new_user(serializer.validated_data)
        tokens = get_tokens_for_user(new_user)
        return Response({'message': 'user created', 'tokens': tokens})


class UserLoginApi(APIView):

    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = get_user(email)
            if check_password(password, user.password):
                return Response({'tokens': get_tokens_for_user(user)})
            raise AuthenticationFailed('wrong username or password')
        except:
            raise AuthenticationFailed('wrong username or password')


class Artist(APIView):

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = "__all__"

    def get(self, request):
        artists = get_all_artists()
        return Response(self.OutputSerializer(instance=artists, many=True).data, status=status.HTTP_200_OK)


