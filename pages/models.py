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


class OrganizationSubscription(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        limit_choices_to={'user_type': 'student'},
    )
    organization = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscribers',
        limit_choices_to={'user_type': 'organization'},
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'organization')

    def __str__(self):
        return f'{self.student} follows {self.organization}'
