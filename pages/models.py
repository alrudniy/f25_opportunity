from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

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

class Opportunity(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    organization = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='opportunities',
        limit_choices_to={'user_type': 'organization'},
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def send_new_opportunity_notification(self):
        """Sends an email to all followed students about this new opportunity."""
        # In a real app, you'd fetch students who follow this organization
        # For now, we'll send to all students
        students = models.User.get_users_by_type(models.User.UserType.STUDENT)
        subject = f"New Opportunity: {self.title}"
        message = f"An organization you follow has posted a new opportunity:\n\n{self.title}\n{self.description}\n\nView it here: /opportunities/{self.id}/"
        html_message = render_to_string('emails/new_opportunity.html', {
            'opportunity': self,
            'organization_name': self.organization.display_name,
            'base_url': settings.BASE_URL if hasattr(settings, 'BASE_URL') else 'http://localhost:8000',
        })

        for student in students:
            student.send_email(subject, message, html_message=html_message)

class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]
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
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Application for {self.opportunity.title} by {self.student.display_name}"

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if not is_new and self.status != 'pending':
            self.send_status_change_email()

    def send_status_change_email(self):
        """Sends an email to the student when their application status changes."""
        subject = f"Application Status Update: {self.opportunity.title}"
        message = f"The status of your application for '{self.opportunity.title}' has been updated to: {self.get_status_display()}"
        html_message = render_to_string('emails/application_status_update.html', {
            'application': self,
            'student_name': self.student.display_name,
            'opportunity_title': self.opportunity.title,
            'new_status': self.get_status_display(),
            'base_url': settings.BASE_URL if hasattr(settings, 'BASE_URL') else 'http://localhost:8000',
        })
        self.student.send_email(subject, message, html_message=html_message)

class ChatMessage(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages',
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages',
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.display_name} to {self.receiver.display_name}"

    def send_new_reply_notification(self):
        """Sends an email to the receiver about a new chat message."""
        if not self.read:
            subject = f"New Message from {self.sender.display_name}"
            message = f"You have received a new message from {self.sender.display_name}:\n\n{self.content}"
            html_message = render_to_string('emails/new_chat_reply.html', {
                'message': self,
                'sender_name': self.sender.display_name,
                'receiver_name': self.receiver.display_name,
                'content': self.content,
                'timestamp': self.timestamp,
                'base_url': settings.BASE_URL if hasattr(settings, 'BASE_URL') else 'http://localhost:8000',
            })
            self.receiver.send_email(subject, message, html_message=html_message)

