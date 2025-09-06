from rest_framework import serializers
from userprofile.models import UserProfile
from .models import (
    Room,
    GroupRoom,
    OnlineUser,
    RoomMessage,
    ChatAttachment,
    GroupRoomMessage,
    Reaction,
)


class ReactionUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'first_name', 'last_name', 'image']


class ReactionSerializer(serializers.ModelSerializer):
    profile = ReactionUsersSerializer(read_only=True)

    class Meta:
        model = Reaction
        fields = '__all__'
        read_only_fields = ('updated_at', 'created_at', 'profile')


class GroupRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupRoom
        fields = '__all__'


class AllOnlineStatuserializer(serializers.ModelSerializer):
    online_status = serializers.SerializerMethodField()

    def get_online_status(self, obj):
        return True

    class Meta:
        model = OnlineUser
        fields = ['profile', 'online_status']


class ProfileInformationUpdateOnlineStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'is_online',)


class ChatAttachmentSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        file = self.context['request'].FILES.get('file')

        validated_data['file'] = file
        attachments = ChatAttachment.objects.create(file=file)
        attachments.file_name = attachments.file.name
        attachments.file_size = attachments.file.size
        attachments.save()
        return attachments

    class Meta:
        model = ChatAttachment
        fields = ('id', 'file', 'file_name', 'file_size')
        read_only_fields = ('updated_at', 'created_at',
                            'file_name', 'file_size')


class GroupRoomMessageSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='profile.first_name')
    last_name = serializers.CharField(source='profile.last_name')
    image = serializers.FileField(source='profile.image')
    attachment = ChatAttachmentSerializer(read_only=True)
    reactions = ReactionSerializer(read_only=True, many=True)

    class Meta:
        model = GroupRoomMessage
        fields = '__all__'


class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

    def validate(self, attrs):
        owner = attrs.get('owner')
        partner = attrs.get('partner')
        request = self.context.get('request')

        if owner == partner:
            raise serializers.ValidationError(
                "Owner can't add himself in room")

        if owner != request.user.profile:
            raise serializers.ValidationError(
                "Invalid owner, give requested user's profile id in owner")

        return super().validate(attrs)

    def create(self, validated_data):
        owner = validated_data.get('owner')
        partner = validated_data.get('partner')
        room = Room.objects.filter(owner=owner, partner=partner).first()
        if room:
            return room
        return super().create(validated_data)


class ListRoomSerializer(serializers.ModelSerializer):

    """
        This serializer is used to list the updated chat rooms of the user
    """

    response = serializers.SerializerMethodField()

    def get_response(self, obj):

        user = self.context.get('user')

        try:
            partner = {}

            ### dynamic fields for the UPDATE ROOM API of the partners ###

            partner['partner_id'] = obj.partner.id
            partner['room_id'] = obj.id
            partner['partner_username'] = obj.partner.user.username
            partner['partner_first_name'] = obj.partner.first_name
            partner['partner_last_name'] = obj.partner.last_name
            partner['partner_image'] = obj.partner.image.url if obj.partner.image else None
            partner['partner_is_online'] = obj.partner.is_online
            room_message = RoomMessage.objects.filter(
                room=obj,
            ).last()

            if room_message:
                partner['last_message'] = room_message.message
                partner['last_message_time'] = room_message.created_at

                if room_message.owner == user.profile:

                    partner['is_my_msg'] = True
                else:
                    partner['is_my_msg'] = False
            else:
                partner['partner_last_message'] = None

            ### dynamic fields for the UPDATE ROOM API of the owner ###

            partner['room_created_at'] = obj.created_at.strftime(
                "%Y-%m-%d %H:%M:%S")
            partner['owner_id'] = obj.owner.id
            partner['room_id'] = obj.id
            partner['owner_username'] = obj.owner.user.username
            partner['owner_first_name'] = obj.owner.first_name
            partner['owner_last_name'] = obj.owner.last_name
            partner['owner_image'] = obj.owner.image.url if obj.owner.image else None
            room_message = RoomMessage.objects.filter(
                room=obj,

            ).last()

            if room_message:
                partner['last_message'] = room_message.message
                partner['last_message_time'] = room_message.created_at.strftime(
                    "%Y-%m-%d %H:%M:%S")

                if room_message.owner == user.profile:
                    partner['is_my_msg'] = True

                else:
                    partner['is_my_msg'] = False

            else:
                partner['owner_last_message'] = None

            return partner
        except Exception as e:
            raise Exception(e)

    class Meta:
        model = Room
        fields = ['response']


class RoomMessageSerializer(serializers.ModelSerializer):
    """
        This serializer is used to list the messages of the room
    """

    first_name = serializers.CharField(
        source='owner.first_name', read_only=True)
    last_name = serializers.CharField(source='owner.last_name', read_only=True)
    image = serializers.FileField(source='owner.image', read_only=True)
    reactions = ReactionSerializer(read_only=True, many=True)

    class Meta:
        model = RoomMessage
        fields = '__all__'


class RoomMessageSerializer(serializers.ModelSerializer):
    """
        This serializer is used to list the messages of the room

    """
    attachment = ChatAttachmentSerializer(read_only=True)
    image = serializers.FileField(source='owner.image', read_only=True)
    last_name = serializers.CharField(source='owner.last_name', read_only=True)
    first_name = serializers.CharField(
        source='owner.first_name', read_only=True)
    user_name = serializers.CharField(
        source='owner.user.username', read_only=True)
    reactions = ReactionSerializer(read_only=True, many=True)

    class Meta:
        model = RoomMessage
        fields = [
            'id',
            'image',
            'room',
            'owner',
            'is_file',
            'is_read',
            'message',
            'last_name',
            'user_name',
            'attachment',
            'first_name',
            'created_at',
            'updated_at',
            'reactions',
        ]
