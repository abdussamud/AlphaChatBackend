from django.db import models


class NotificationImage(models.Model):
    image = models.FileField(upload_to='notification_images/')