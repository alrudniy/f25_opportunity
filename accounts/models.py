from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    class UserType(models.TextChoices):
        STUDENT = 'student', 'Student'
        ORGANIZATION = 'organization', 'Organization'
        # ADMINISTRATOR = 'administrator', 'Administrator' # Uncomment if needed

    user_type = models.CharField(
        max_length=15,
        choices=UserType.choices,
        default=UserType.STUDENT,
    )

    # Profile fields, can be managed directly on the User model.
    # Note: Django's AbstractUser already includes first_name and last_name.
    # We ensure they are visible in the model definition for form editing.
    # For more complex profile management, consider a separate Profile model.
    # first_name = models.CharField(_('first name'), max_length=150, blank=True)
    # last_name = models.CharField(_('last name'), max_length=150, blank=True)
    university = models.CharField(max_length=255, blank=True, null=True)
    class_year = models.CharField(max_length=4, blank=True, null=True) # e.g., "2025", "2026"

    # The email field already exists in AbstractUser and is unique=True by default.
    # If you want email to be the login username, you'll need to adjust AUTH_USER_MODEL, LOGIN_URL, etc.
    # and potentially REQUIRED_FIELDS.
    # email = models.EmailField(_('email address'), unique=True)
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username'] # If email is USERNAME_FIELD, username might not be required or needs adjustment.

    def save(self, *args, **kwargs):
        # If it's a new user and user_type is not set, default to STUDENT.
        if not self.pk and not self.user_type:
            self.user_type = self.UserType.STUDENT
        super().save(*args, **kwargs)

    @property
    def display_name(self):
        # Prioritize first_name and last_name, fall back to username if empty.
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.username

# If you prefer to use a separate Profile model, uncomment the following block:
# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
#     university = models.CharField(max_length=255, blank=True, null=True)
#     class_year = models.CharField(max_length=4, blank=True, null=True) # e.g., "2025", "2026"
#
#     def __str__(self):
#         return f"{self.user.display_name}'s Profile"
