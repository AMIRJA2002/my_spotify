from .services import create_new_playlist, delete_playlist, add_to_playlist, remove_from_playlist
from spotify_app.common.permissions import IsOwnerOrReadOnly
from spotify_app.music.apis import UploadSongAndAddToAlbum
from .selectors import get_playlist, get_single_playlist
from rest_framework.permissions import IsAuthenticated
from .models import PlayList, AddSongAndDateAdded
from spotify_app.music.models import MusicUpload
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework import status


class CreatePlayListApi(APIView):
    permission_classes = [IsAuthenticated]
    
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = PlayList
            fields = '__all__'

    def post(self, request):
        new_playlist = create_new_playlist(user=request.user)
        return Response(self.OutputSerializer(instance=new_playlist).data, status=status.HTTP_201_CREATED)


class UpdatePlayListApi(APIView):
    permission_classes = [IsAuthenticated]

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = PlayList
            fields = '__all__'

    def patch(self, request, **kwargs):
        playlist = get_single_playlist(id=kwargs.get('playlist_id', None), user=request.user)
        serializer = self.OutputSerializer(instance=playlist, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class DeletePlaylistApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):
        delete_playlist(request.user, kwargs.get('playlist_id'))
        return Response({'message': 'deleted'}, status=status.HTTP_200_OK)


class AddMusicToPlaylistApi(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    class InputSerializer(serializers.Serializer):
        playlist = serializers.IntegerField()
        song = serializers.IntegerField()

    class OutputSerializer(serializers.ModelSerializer):
        music = serializers.SerializerMethodField()

        class Meta:
            model = AddSongAndDateAdded
            fields = '__all__'

        def get_music(self, obj):
            test = MusicUpload.objects.filter(songs__playlist=obj.playlist)
            return UploadSongAndAddToAlbum.OutputSerializer(test, many=True).data

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_playlist = add_to_playlist(serializer.validated_data)
        if not updated_playlist:
            return Response({'message': 'song is already in your playlist'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.OutputSerializer(updated_playlist).data, status=status.HTTP_201_CREATED)


class DeleteMusicFromPlaylistApi(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    class InputSerializer(serializers.Serializer):
        playlist = serializers.IntegerField()
        song = serializers.IntegerField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        modify_playlist = remove_from_playlist(serializer.validated_data)
        if not modify_playlist:
            return Response({'message': 'this song is not in your playlist'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'deleted'}, status=status.HTTP_200_OK)


class UserPlaylistsApi(APIView):
    permission_classes = [IsAuthenticated]

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = PlayList
            fields = '__all__'

    def get(self, request):
        playlist_id = request.POST.get('id', None)
        playlist = get_playlist(request.user, playlist_id)
        return Response(self.OutputSerializer(playlist, many=True).data, status=status.HTTP_200_OK)


class UserPlaylistDetailApi(APIView):
    permission_classes = [IsAuthenticated]

    class OutputSerializer(serializers.ModelSerializer):
        songs = serializers.SerializerMethodField()

        class Meta:
            model = PlayList
            fields = '__all__'

        def get_songs(self, playlist):
            songs_date = playlist.date_added.all()
            print(songs_date, 40 * '100')
            return AddMusicToPlaylistApi.OutputSerializer(songs_date, many=True).data

    def post(self, request):
        playlist = get_playlist(request.user, request.data['playlist_id'])
        return Response(self.OutputSerializer(playlist).data, status=status.HTTP_200_OK)
