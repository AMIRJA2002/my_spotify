from .selectors import return_all_musics_or_specific_number_number, get_artist_albums, get_albums, get_artist, \
    get_top_ten_list, get_top_ten
from rest_framework.permissions import IsAuthenticated, AllowAny
from spotify_app.common.permissions import IsOwnerOrReadOnly
from .services import create_album, add_music, create_artist_profile, create_top_ten_list, delete_music_from_top_ten
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework import status
from .models import Album, MusicUpload, SingerProfile, TopTenSongForArtist


class AddAlbum(APIView):
    permission_classes = [IsAuthenticated]

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Album
            fields = ('name', 'release_date', 'cover')

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Album
            fields = ('name', 'singer', 'release_date', 'cover', 'songs_number', 'like_count')

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
            fields = ('name', 'cover', 'release_data', 'song', 'album', 'genre', 'happy_or_sad')

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


class ReturnAllMusic(APIView):
    permission_classes = [AllowAny]

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = MusicUpload
            fields = ('id', 'singer', 'name', 'release_data', 'duration', 'song', 'cover')

    def get(self, request):
        number_of_music = request.GET.get('number', None)
        musics = return_all_musics_or_specific_number_number(number_of_music)
        print(musics)
        print(self.OutputSerializer(musics, many=True).data)
        return Response(self.OutputSerializer(musics, many=True).data, status=status.HTTP_200_OK)


class Albums(APIView):
    permission_classes = (IsAuthenticated,)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Album
            fields = "__all__"

    def get(self, request):
        album_id = request.POST.get('id', None)
        albums = get_albums(album_id)
        serializer = self.OutputSerializer(instance=albums, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ArtistAlbum(APIView):
    permission_classes = (IsAuthenticated,)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Album
            fields = "__all__"

    def get(self, request):
        albums = get_artist_albums(request.user)
        serializer = self.OutputSerializer(instance=albums, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ArtistProfileView(APIView):

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = SingerProfile
            fields = ('name', 'image')

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = SingerProfile
            fields = '__all__'

    def get(self, request):
        artist_id = request.POST.get('id', None)
        artist_profile = get_artist(artist_id)
        return Response(self.OutputSerializer(artist_profile).data, status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.roll != 0:
            return Response({'msg': 'you are not a singer'}, status=status.HTTP_400_BAD_REQUEST)
        data = self.InputSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        artist_profile = create_artist_profile(request, data)
        return Response(self.OutputSerializer(artist_profile).data, status=status.HTTP_201_CREATED)

    def patch(self, request):
        artist_profile = get_artist(request)
        serializer = self.OutputSerializer(instance=artist_profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateTopTenView(APIView):
    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = TopTenSongForArtist
            fields = ('music',)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = TopTenSongForArtist
            fields = '__all__'

    def get(self, request, *args, **kwargs):
        artist_id = request.POST.get('id', None)
        top_ten_list = get_top_ten_list(artist_id)
        return Response(self.OutputSerializer(top_ten_list, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        data = self.InputSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        top_ten_list = create_top_ten_list(request, data)
        return Response(self.OutputSerializer(top_ten_list).data, status=status.HTTP_201_CREATED)

    def patch(self, request):
        top_ten = get_top_ten(request)
        serializer = self.OutputSerializer(instance=top_ten, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        music_id = request.POST.get('id', None)
        delete_music_from_top_ten(request, music_id)
        return Response({'msg': 'deleted'}, status=status.HTTP_200_OK)
