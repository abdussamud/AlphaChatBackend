from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from userprofile.serializers import UserProfileSerializer

User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['username', 'email',  'user_type', 'profile']
