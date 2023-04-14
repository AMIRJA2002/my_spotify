from rest_framework.permissions import IsAuthenticated
from .services import create_album, add_music
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework import status
from .models import Album, Music


class AddAlbum(APIView):

    permission_classes = [IsAuthenticated]

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Album
            fields = ('release_date', 'cover')

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Album
            fields = ('singer', 'release_date', 'cover', 'songs_number', 'like_count')

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_album = create_album(serializer.validated_data, request.user)

        return Response(self.OutputSerializer(new_album).data)


class AddMusic(APIView):

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Music
            fields = ('singer', 'album', 'cover', 'name', 'release_date', 'music')

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Music
            fields = '__all__'

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_music = add_music(serializer.validated_data)
        return Response(self.OutputSerializer(new_music).data)

