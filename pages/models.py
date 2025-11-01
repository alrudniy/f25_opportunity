from django.conf import settings
from django.db import models


# Create your models here.
class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    university = models.CharField(max_length=255, blank=True)
    class_year = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Experience(models.Model):
    class ExperienceType(models.TextChoices):
        VOLUNTEER = 'volunteer', 'Volunteer'
        INTERNSHIP = 'internship', 'Internship'
        CAREER = 'career', 'Career'

    profile = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='experiences')
    organization_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField()
    experience_type = models.CharField(max_length=20, choices=ExperienceType.choices)
    auto_added = models.BooleanField(default=False)
    source = models.CharField(max_length=50, default='manual')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role} at {self.organization_name}"

    class Meta:
        ordering = ['-start_date']
