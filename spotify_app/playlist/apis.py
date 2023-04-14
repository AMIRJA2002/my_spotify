from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .services import create_new_playlist, update_playlist, delete_playlist
from .selectors import get_playlist
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework import status
from .models import PlayList


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



class AddMusicToPlaylist(APIView):
    ...





























