from django.contrib import admin
from .models import (
    Room,
    OnlineUser,
    RoomMessage,
    GroupRoom,
    ChatAttachment,
    GroupRoomMessage,
    Reaction,
)

# Register your models here.


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'profile', 'message', 'reaction', 'created_at']


@admin.register(GroupRoom)
class GroupRoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']


admin.site.register(ChatAttachment)


@admin.register(GroupRoomMessage)
class GroupRoomMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'room', 'profile',
                    'message', 'is_read', 'is_file', 'created_at']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'partner', 'created_at']


@admin.register(RoomMessage)
class RoomMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'room', 'owner', 'message',
                    'is_read', 'is_file', 'created_at']


@admin.register(OnlineUser)
class OnlineUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'profile', 'channel_id', 'created_at']
