from django.db import models


class NotificationDetails(models.Model):
    sender = models.ForeignKey(
        "userprofile.UserProfile", on_delete=models.CASCADE, related_name="sender_notification")
    receiver = models.ForeignKey('userprofile.UserProfile', on_delete=models.CASCADE, related_name="receiver_notification")
    heading = models.CharField(max_length=100, blank=True, null=True)
    plain_text = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    notification_type = models.CharField(max_length=255)
    notification_created_at = models.DateTimeField(auto_now_add=True)
    notification_updated_at = models.DateTimeField(auto_now=True)
    notification_is_read = models.BooleanField(default=False)
    notification_is_deleted = models.BooleanField(default=False)
    notification_is_archived = models.BooleanField(default=False)
