from django.db.models import Q
from userprofile.models import UserProfile
from django.shortcuts import get_object_or_404
from channels.db import database_sync_to_async
from django.template.defaultfilters import slugify

from .models import (
    Room,
    OnlineUser,
    RoomMessage,
    GroupRoom,
    ChatAttachment,
    GroupRoomMessage,
)
from .serializers import (
    ListRoomSerializer,
    RoomMessageSerializer,
    AllOnlineStatuserializer,
    GroupRoomMessageSerializer,
)
"""
    This function is used to check whether the user is the 
    member of the workspace room or not.
"""


@database_sync_to_async
def get_chat_rooms_updated(user, request):
    """ 
        This function is used to get updated chat rooms of the user 
    """

    rooms = Room.objects.filter(
        Q(owner=user.profile) | Q(partner=user.profile)
    )

    rooms_serializer = ListRoomSerializer(
        rooms, many=True, context={'request': request, 'user': user})

    return rooms_serializer.data


@database_sync_to_async
def is_group_room_member(user, group):
    try:
        group = GroupRoom.objects.get(id=group)
        is_member = group.profile.filter(user=user).exists()
        return is_member, group
    except:
        return False, None


"""
    This function is used to create the instance of WorkspaceRoomMessage class
    when the message in set in activity chat
"""


@database_sync_to_async
def get_attachment_object(attachment):
    file_attachment_object = get_object_or_404(ChatAttachment, id=attachment)
    return file_attachment_object


@database_sync_to_async
def create_ws_room_msg_object(workspace, user, message, is_file, file_attachment):
    workspace_room = get_object_or_404(GroupRoom, id=workspace)
    _attachment = None
    if is_file:
        _attachment = get_object_or_404(ChatAttachment, pk=file_attachment)

    message_obj = GroupRoomMessage.objects.create(
        room=workspace_room,
        profile=user.profile,
        message=message,
        is_file=is_file,
        attachment=_attachment,


    )
    message_ser = GroupRoomMessageSerializer(message_obj)
    return message_ser.data


"""
    This function is used to check wheather the user is the 
    member of the room or not.
"""


@database_sync_to_async
def is_room_member(user, room_id):
    rooms = Room.objects.filter(
        Q(id=room_id) & (Q(owner=user.profile) | Q(partner=user.profile))
    )
    print(rooms)
    if rooms.exists():
        room = rooms.first()
        group_name = slugify(
            f'{room.owner.user.username}-'
            f'{room.partner.user.username}-{room.id}')
        return True, group_name
    return False, None


"""
    This function is used to create the instance of RoomMessage class
    when the message in set in private chat
"""
search_field_for_partner = [

    'partner__last_name',
    'partner__first_name',
    'partner__user__username',

]


@database_sync_to_async
def create_room_message_object(room, message, is_file, user, file_attachment):
    room = get_object_or_404(Room, id=room)
    _attachment = None
    if is_file:
        _attachment = get_object_or_404(ChatAttachment, pk=file_attachment)
    job_offer_obj = None
    message_obj = RoomMessage.objects.create(
        room=room,
        owner=user.profile,
        message=message,
        is_file=is_file,
        attachment=_attachment,

    )
    message_ser = RoomMessageSerializer(message_obj)
    return message_ser.data


"""
    This function is used to create the instance of OnlineUser class
    whenever a login user open a new tab
"""


@database_sync_to_async
def create_online_user_instance(channel_name, user):
    online_user = OnlineUser.objects.create(
        profile=user.profile,
        channel_id=channel_name
    )
    user = UserProfile.objects.get(user=user)
    user.is_online = True

    user.save()
    return online_user


"""
    This function is used to check wheather a user is online or not
"""


@database_sync_to_async
def all_online_users(channel_name):
    online_users = OnlineUser.objects.all().distinct('profile')
    serilazer = AllOnlineStatuserializer(online_users, many=True)
    return serilazer.data


@database_sync_to_async
def is_user_online(user):
    user_profile = get_object_or_404(UserProfile, id=user.profile.id)

    if user_profile.is_online:

        return True
    return False


@database_sync_to_async
def is_user_online_check(user_profile_id):
    user_profile = get_object_or_404(UserProfile, id=user_profile_id)

    if user_profile.is_online:
        return True
    return False


"""
    This function is used to set user as online
"""


@database_sync_to_async
def set_user_online(user):
    user_profile = get_object_or_404(UserProfile, id=user.profile.id)
    user_profile.is_online = True
    user_profile.save()
    return user_profile


"""
    This function is used to delete the instance of OnlineUser class
    It return the is_online status 'False' if the user is offline
"""


@database_sync_to_async
def delete_online_user_instance(user):

    OnlineUser.objects.filter(
        profile=user.profile,
    ).delete()

    return user.profile.id


@database_sync_to_async
def delete_online_user_instance_check(user):

    user_profile = get_object_or_404(UserProfile, id=user.profile.id)
    user_profile.is_online = False
    user_profile.save()
    return False
