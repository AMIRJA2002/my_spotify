from .services import create_new_playlist, update_playlist, delete_playlist, add_to_playlist, remove_to_playlist
from spotify_app.common.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from .models import PlayList, AddSongAndDateAdded
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from .selectors import get_playlist
from rest_framework import status


class CreatePlayListApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        create_new_playlist(user=request.user)
        return Response({'message': f'new playlist for: {request.user.email}'}, status=status.HTTP_201_CREATED)


class UpdatePlayListApi(APIView):
    permission_classes = [IsAuthenticated]

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = PlayList
            fields = ('name', 'image', 'description')

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = PlayList
            fields = ('name', 'description', 'image')

    def patch(self, request, **kwargs):
        serializer = self.InputSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        playlist = get_playlist(request.user, kwargs.get('playlist_id'))
        updated_playlist = update_playlist(serializer.validated_data, playlist)
        return Response(self.OutputSerializer(updated_playlist).data)


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
        class Meta:
            model = AddSongAndDateAdded
            fields = '__all__'

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
        modify_playlist = remove_to_playlist(serializer.validated_data)
        if not modify_playlist:
            return Response({'message': 'this song is not in your playlist'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'deleted'}, status=status.HTTP_200_OK)
