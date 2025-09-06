from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from .serializers import (
    GroupRoomSerializer,
    ReactionSerializer,
)
from .models import (
    GroupRoom,
    Reaction,
)


class ReactionViewSet(viewsets.ModelViewSet):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer

    def get_queryset(self):
        message_id = self.request.query_params.get('message_id', None)
        return Reaction.objects.filter(message=message_id)

    def create(self, request, *args, **kwargs):
        serializer = ReactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(profile=request.user.profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GroupRoomViewSet(viewsets.ModelViewSet):
    queryset = GroupRoom.objects.all()
    serializer_class = GroupRoomSerializer

    def get_queryset(self):
        user = self.request.user
        return GroupRoom.objects.filter(profile=user.profile)

    def create(self, request, *args, **kwargs):
        serializer = GroupRoomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(group_creator=request.user.profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.group_admin.filter(user=request.user).exists() or instance.group_moderator.filter(
                user=request.user).exists():
            serializer = self.get_serializer(
                instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({'message': "you are not be able to do..."}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.group_admin.filter(user=request.user).exists() or instance.group_moderator.filter(
                user=request.user).exists():
            instance.delete()
            return Response({"message": "Group deleted"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': "you are not be able to do..."}, status=status.HTTP_401_UNAUTHORIZED)


class AddAndRemoveGroupMemberAPIView(UpdateAPIView):
    """
    This View is used to add and remove the members of the group
    permission_classes:
        IsAuthenticated
    Parameters:
        id: int
    Returns:
        profile: object

    """
    serializer_class = GroupRoomSerializer
    model = GroupRoom
    lookup_field = 'pk'

    def get_queryset(self):
        return GroupRoom.objects.filter(profile=self.request.user.profile)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.group_admin.filter(user=request.user).exists() or instance.group_moderator.filter(
                user=request.user).exists():
            is_remove = request.data.get('is_remove', None)
            if instance.group_creator == request.user.profile and is_remove:
                return Response({'message': "You are not be able to remove creator from group..."},
                                status=status.HTTP_401_UNAUTHORIZED)
            if instance.group_admin.filter(user=request.user).exists() and is_remove:
                return Response({'message': "You are not be able to remove admin from group..."},
                                status=status.HTTP_401_UNAUTHORIZED)
            if instance.group_moderator.filter(
                    user=request.user).exists() and is_remove:
                return Response({'message': "You are not be able to remove moderator from group..."},
                                status=status.HTTP_401_UNAUTHORIZED)
            if instance.profile.filter(id=request.data.get('profile')).exists():
                return Response({'message': "This user is already member of this group..."},
                                status=status.HTTP_401_UNAUTHORIZED)

            if is_remove:
                instance.profile.remove(request.data.get('profile'))
            else:
                instance.profile.add(request.data.get('profile'))
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': "you are not be able to do..."}, status=status.HTTP_401_UNAUTHORIZED)
