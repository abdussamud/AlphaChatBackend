from django.db import models


# Create your models here.
class GroupRoom(models.Model):

    profile = models.ManyToManyField(
        "userprofile.UserProfile", related_name='profile_rooms')
    group_creator = models.ForeignKey(
        "userprofile.UserProfile", on_delete=models.CASCADE, related_name='creator_rooms')
    group_admin = models.ManyToManyField(
        'userprofile.UserProfile', related_name='group_admin_rooms')
    group_moderator = models.ManyToManyField(
        'userprofile.UserProfile', related_name='group_moderator_rooms')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ChatAttachment(models.Model):
    file = models.FileField(upload_to="chat-attachments")
    file_name = models.CharField(max_length=255, blank=True, null=True)
    file_size = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


REACTION_CHOICES = (
    ('like', 'like'),
    ('love', 'love'),
    ('haha', 'haha'),
    ('wow', 'wow'),
    ('sad', 'sad'),
    ('angry', 'angry'),
)


class Reaction(models.Model):
    profile = models.ForeignKey(
        "userprofile.UserProfile", on_delete=models.CASCADE, related_name='profile_reactions')
    room_message = models.ForeignKey(
        "chat.GroupRoomMessage", on_delete=models.CASCADE, related_name='room_message_reactions', null=True, blank=True)
    message = models.ForeignKey(
        "chat.RoomMessage", on_delete=models.CASCADE, related_name='message_reactions', null=True, blank=True)
    reaction = models.CharField(
        max_length=255, choices=REACTION_CHOICES, default='like')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class GroupRoomMessage(models.Model):
    room = models.ForeignKey(
        GroupRoom, on_delete=models.CASCADE, related_name='ws_room_messages')
    profile = models.ForeignKey(
        "userprofile.UserProfile", on_delete=models.CASCADE, related_name='profile_ws_room_messages')
    message = models.TextField(max_length=1000, null=True, blank=True)
    reactions = models.ManyToManyField(
        Reaction, related_name='reaction_ws_room_messages', blank=True)

    attachment = models.ForeignKey(ChatAttachment, on_delete=models.CASCADE,
                                   related_name='attachment_ws_room_messages', null=True, blank=True)
    is_file = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    is_offer_attached = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Room(models.Model):
    owner = models.ForeignKey(
        "userprofile.UserProfile", on_delete=models.CASCADE, related_name='owner_rooms')
    partner = models.ForeignKey(
        "userprofile.UserProfile", on_delete=models.CASCADE, related_name='partner_rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RoomMessage(models.Model):
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name='room_messages', null=True, blank=True)
    owner = models.ForeignKey(
        "userprofile.UserProfile", on_delete=models.CASCADE, related_name='owner_room_messages', null=True, blank=True)
    message = models.TextField(max_length=1000, null=True, blank=True)
    attachment = models.ForeignKey(ChatAttachment, on_delete=models.CASCADE,
                                   related_name='attachment_room_messages', null=True, blank=True)
    reactions = models.ManyToManyField(
        Reaction, related_name='reaction_room_messages', blank=True)
    is_file = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OnlineUser(models.Model):
    profile = models.ForeignKey(
        "userprofile.UserProfile",
        on_delete=models.CASCADE,
        related_name='online_profile',
        blank=True,
        null=True)
    channel_id = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
