from django.db import models
from django.conf import settings

# We will likely need to import your Opportunity model here.
# For example: from opportunities.models import Opportunity

class Conversation(models.Model):
    """
    A conversation between two or more users.
    For this use case, it will be between a student and an organization.
    """
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='conversations'
    )
    # opportunity = models.ForeignKey(Opportunity, null=True, blank=True, on_delete=models.SET_NULL, related_name='conversations')

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        usernames = [user.get_username() for user in self.participants.all()]
        return f"Conversation between {', '.join(usernames)}"


class Message(models.Model):
    """A message in a conversation."""
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('timestamp',)

    def __str__(self):
        return f"From {self.sender.get_username()} on {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
