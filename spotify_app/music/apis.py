from rest_framework.permissions import IsAuthenticated
from spotify_app.common.permissions import IsOwnerOrReadOnly
from .services import create_album, add_music
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework import status
from .models import Album, MusicUpload


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


class UploadSongAndAddToAlbum(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = MusicUpload
            fields = ('name', 'cover', 'release_data', 'song', 'album')

        def validate_song(self, value):
            if not value.name.endswith('.mp3'):
                raise serializers.ValidationError('The file format must be mp3')
            return value

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = MusicUpload
            fields = '__all__'

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_music = add_music(serializer.validated_data, request)
        return Response(self.OutputSerializer(new_music).data, status=status.HTTP_201_CREATED)
