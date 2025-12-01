from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_organizations",
    )
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="following_organizations", blank=True
    )


class OrganizationUpdate(models.Model):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="updates"
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new:
            from feeds.models import FeedItem

            content_type = ContentType.objects.get_for_model(self)
            for follower in self.organization.followers.all():
                FeedItem.objects.create(
                    user=follower, content_type=content_type, object_id=self.id
                )
