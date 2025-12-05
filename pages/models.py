from django.db import models
from django.conf import settings
from django.utils import timezone

class Opportunity(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    organization = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posted_opportunities',
        limit_choices_to={'user_type': 'organization'},
    )
    # Add more fields as needed, e.g., deadline, location, skills_required

    def __str__(self):
        return self.title


class Application(models.Model):
    class ApplicationStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        ACCEPTED = 'accepted', 'Accepted'
        REJECTED = 'rejected', 'Rejected'
        COMPLETED = 'completed', 'Completed'

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='applications',
        limit_choices_to={'user_type': 'student'},
    )
    opportunity = models.ForeignKey(
        Opportunity,
        on_delete=models.CASCADE,
        related_name='applications',
    )
    status = models.CharField(
        max_length=10,
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.PENDING,
    )
    applied_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'opportunity')

    def save(self, *args, **kwargs):
        # Check if the status is changing to 'completed'
        if self.pk:  # object already exists
            old_application = Application.objects.get(pk=self.pk)
            if old_application.status != self.status and self.status == self.ApplicationStatus.COMPLETED:
                # Create an experience entry
                Experience.objects.create(
                    student=self.student,
                    opportunity=self.opportunity,
                    title=f"Completed {self.opportunity.title}",
                    description=self.opportunity.description,
                    date_completed=timezone.now().date(),
                )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.username} - {self.opportunity.title} ({self.get_status_display()})"


class Experience(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,  # If opportunity is deleted, experience can remain
        null=True,
        blank=True,
        related_name='experiences',
    )
    opportunity = models.ForeignKey(
        Opportunity,
        on_delete=models.SET_NULL,  # If opportunity is deleted, experience can remain
        null=True,
        blank=True,
        related_name='experiences',
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_completed = models.DateField()

    def __str__(self):
        return self.title

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
