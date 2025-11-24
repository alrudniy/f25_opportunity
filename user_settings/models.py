from django.db import models
from django.conf import settings

class UserSettings(models.Model):
    THEME_CHOICES = (
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('auto', 'Auto'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='settings')
    receive_updates = models.BooleanField(default=True)
    public_experience = models.BooleanField(default=True)
    notifications_on = models.BooleanField(default=True)
    theme = models.CharField(max_length=5, choices=THEME_CHOICES, default='auto')

    def __str__(self):
        return f"Settings for {self.user.username}"
