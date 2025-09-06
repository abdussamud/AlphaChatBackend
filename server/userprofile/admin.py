from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'phone',
                    'address', 'image', 'created_at', 'updated_at', 'is_online')
    list_filter = ('user', 'first_name', 'last_name', 'phone',
                   'address', 'image', 'created_at', 'updated_at', 'is_online')
    search_fields = ('user', 'first_name', 'last_name', 'phone',
                     'address', 'image', 'created_at', 'updated_at', 'is_online')


# Register your models here.
