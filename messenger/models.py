from django.db import models

class Volunteer(models.Model):
    """
    A placeholder model for a volunteer.
    In a real application, this would likely have more fields
    and be integrated with a user authentication system.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class Organization(models.Model):
    """
    A placeholder model for an organization.
    In a real application, this would likely have more fields
    and be integrated with a user authentication system.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name
