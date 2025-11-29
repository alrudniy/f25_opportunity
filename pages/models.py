from django.db import models
from django.conf import settings

# Create your models here.
class Achievement(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='achievements',
        limit_choices_to={'user_type': 'student'},
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_completed = models.DateField()

    def __str__(self):
        return self.title

class FindOpportunity(models.Model):
    class OpportunityType(models.TextChoices):
        VOLUNTEER = 'volunteer', 'Volunteer'
        INTERNSHIP = 'internship', 'Internship'

    class OpportunityStatus(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'
        ARCHIVED = 'archived', 'Archived'
        CLOSED = 'closed', 'Closed'

    # Basic information
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField(blank=True, help_text="Skills, experience, or prerequisites needed")

    # Type and organization
    opportunity_type = models.CharField(
        max_length=20,
        choices=OpportunityType.choices,
        default=OpportunityType.VOLUNTEER
    )
    organization = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='opportunities',
        limit_choices_to={'user_type': 'organization'},
    )

    # Location
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    is_remote = models.BooleanField(default=False)

    # Dates
    application_deadline = models.DateField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    # Capacity and status
    capacity = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Number of available spots"
    )
    status = models.CharField(
        max_length=20,
        choices=OpportunityStatus.choices,
        default=OpportunityStatus.DRAFT
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Opportunities"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.organization.email}"

    def get_location_display(self):
        """Returns a formatted location string"""
        if self.is_remote:
            return "Remote"
        parts = [self.city, self.state]
        location = ", ".join(filter(None, parts))
        return location if location else "Location not specified"
