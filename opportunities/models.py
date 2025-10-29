from django.conf import settings
from django.db import models


class OrganizationProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organization_profile'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class VolunteerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='volunteer_profile'
    )
    skills = models.TextField(blank=True)
    interests = models.TextField(blank=True)

    def __str__(self):
        return self.user.display_name


class Opportunity(models.Model):
    organization = models.ForeignKey(
        OrganizationProfile, on_delete=models.CASCADE, related_name='opportunities'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class OpportunityApplication(models.Model):
    opportunity = models.ForeignKey(
        Opportunity, on_delete=models.CASCADE, related_name='applications'
    )
    volunteer = models.ForeignKey(
        VolunteerProfile, on_delete=models.CASCADE, related_name='applications'
    )
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('opportunity', 'volunteer')

    def __str__(self):
        return f"{self.volunteer} applied for {self.opportunity}"
