from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
from django.conf import settings

class User(AbstractUser):
    class UserType(models.TextChoices):
        STUDENT = 'student', 'Student'
        ORGANIZATION = 'organization', 'Organization'
        ADMINISTRATOR = 'administrator', 'Administrator'

    user_type = models.CharField(max_length=20, choices=UserType.choices, default=UserType.STUDENT)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # keep username for admin compatibility

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)

    @property
    def display_name(self):
        full = f"{self.first_name} {self.last_name}".strip()
        return full if full else self.email

    def send_email(self, subject, message, html_message=None):
        """Helper method to send an email to this user."""
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [self.email],
            html_message=html_message
        )

    @staticmethod
    def get_users_by_type(user_type):
        """Get all users of a specific type."""
        return User.objects.filter(user_type=user_type)

    @staticmethod
    def get_followed_organizations(user):
        """
        Placeholder: In a real application, this would fetch organizations
        that the user is following. For now, it returns all organizations.
        """
        if user.user_type == User.UserType.STUDENT:
            # Assuming a ManyToManyField 'followed_organizations' on User model
            # return user.followed_organizations.all()
            return User.objects.filter(user_type=User.UserType.ORGANIZATION)
        return User.objects.none()

