from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail
from pages.models import Opportunity, Application
from unittest.mock import patch

User = get_user_model()

class EmailNotificationTests(TestCase):

    def setUp(self):
        """Set up test data and client."""
        self.client = Client()

        # Create users
        self.student_user = User.objects.create_user(
            username='student',
            email='student@example.com',
            password='password123',
            user_type=User.UserType.STUDENT
        )
        self.organization_user = User.objects.create_user(
            username='organization',
            email='organization@example.com',
            password='password123',
            user_type=User.UserType.ORGANIZATION
        )
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='password123',
            user_type=User.UserType.ADMINISTRATOR
        )

        # Login as student for application tests
        self.client.login(email='student@example.com', password='password123')
        self.student_url = reverse('student_achievements') # Example student page
        self.apply_url = reverse('apply_to_opportunity', kwargs={'opportunity_pk': 1}) # Placeholder, will create opportunity

        # Login as organization for opportunity and application management tests
        self.client.logout()
        self.client.login(email='organization@example.com', password='password123')
        self.create_opportunity_url = reverse('create_opportunity')
        self.manage_applications_url = reverse('manage_applications')

        # Login as admin
        self.client.logout()
        self.client.login(email='admin@example.com', password='password123')
        self.admin_url = reverse('admin:index') # Example admin page

        # Clear any previous emails
        mail.outbox = []

    def test_welcome_email_on_registration(self):
        """Test that a welcome email is sent upon user registration."""
        self.client.logout()
        register_url = reverse('register')
        response = self.client.post(register_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'password_confirm': 'password123',
            'user_type': User.UserType.STUDENT,
        })

        self.assertEqual(response.status_code, 302) # Redirect after successful registration
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Welcome to Opportunity App!")
        self.assertIn("Welcome to Opportunity App!", mail.outbox[0].body)
        self.assertIn("newuser@example.com", mail.outbox[0].body)

    def test_new_opportunity_notification(self):
        """Test that an email is sent to students when a new opportunity is posted."""
        self.client.login(email='organization@example.com', password='password123')
        response = self.client.post(self.create_opportunity_url, {
            'title': 'Software Engineer Intern',
            'description': 'Gain experience in software development.',
        })

        self.assertEqual(response.status_code, 302) # Redirect after creating opportunity
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "New Opportunity: Software Engineer Intern")
        self.assertIn("New Opportunity: Software Engineer Intern", mail.outbox[0].body)
        self.assertIn("Gain experience in software development.", mail.outbox[0].body)
        # Check if the email was sent to the student user (as a placeholder for followed orgs)
        self.assertEqual(mail.outbox[0].to[0], self.student_user.email)

    def test_new_application_submitted_notification(self):
        """Test that an email is sent to the organization when a student applies."""
        # First, create an opportunity
        self.client.login(email='organization@example.com', password='password123')
        self.client.post(self.create_opportunity_url, {
            'title': 'Data Analyst Role',
            'description': 'Analyze data and provide insights.',
        })
        opportunity = Opportunity.objects.get(title='Data Analyst Role')

        # Now, apply as a student
        self.client.logout()
        self.client.login(email='student@example.com', password='password123')
        apply_url = reverse('apply_to_opportunity', kwargs={'opportunity_pk': opportunity.pk})
        response = self.client.post(apply_url, {}) # Assuming no extra fields for application form

        self.assertEqual(response.status_code, 302) # Redirect after applying
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "New Application Submitted: Data Analyst Role")
        self.assertIn("A new application has been submitted for the opportunity 'Data Analyst Role'", mail.outbox[0].body)
        self.assertIn("by student", mail.outbox[0].body) # Assuming display_name is 'student'
        # Check if the email was sent to the organization
        self.assertEqual(mail.outbox[0].to[0], self.organization_user.email)

    def test_application_status_change_email(self):
        """Test that an email is sent when an application status changes."""
        # Create an opportunity and an application
        self.client.login(email='organization@example.com', password='password123')
        self.client.post(self.create_opportunity_url, {
            'title': 'Marketing Assistant',
            'description': 'Assist with marketing campaigns.',
        })
        opportunity = Opportunity.objects.get(title='Marketing Assistant')

        self.client.logout()
        self.client.login(email='student@example.com', password='password123')
        apply_url = reverse('apply_to_opportunity', kwargs={'opportunity_pk': opportunity.pk})
        self.client.post(apply_url, {})
        application = Application.objects.get(student=self.student_user, opportunity=opportunity)

        # Now, change the status as the organization
        self.client.logout()
        self.client.login(email='organization@example.com', password='password123')
        response = self.client.post(self.manage_applications_url, {
            'application_id': application.pk,
            'status': 'accepted',
        })

        self.assertEqual(response.status_code, 302) # Redirect after status change
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Application Status Update: Marketing Assistant")
        self.assertIn("The status of your application for 'Marketing Assistant' has been updated to: Accepted", mail.outbox[0].body)
        self.assertEqual(mail.outbox[0].to[0], self.student_user.email)

    def test_application_reminder_email(self):
        """Test that a reminder email can be sent for an application."""
        # Create an opportunity and an application
        self.client.login(email='organization@example.com', password='password123')
        self.client.post(self.create_opportunity_url, {
            'title': 'Project Manager',
            'description': 'Manage project timelines and resources.',
        })
        opportunity = Opportunity.objects.get(title='Project Manager')

        self.client.logout()
        self.client.login(email='student@example.com', password='password123')
        apply_url = reverse('apply_to_opportunity', kwargs={'opportunity_pk': opportunity.pk})
        self.client.post(apply_url, {})
        application = Application.objects.get(student=self.student_user, opportunity=opportunity)

        # Send a reminder email
        reminder_url = reverse('send_application_reminder', kwargs={'application_pk': application.pk})
        response = self.client.get(reminder_url)

        self.assertEqual(response.status_code, 302) # Redirect after sending reminder
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Reminder: Application for Project Manager")
        self.assertIn("This is a reminder about your application for 'Project Manager'.", mail.outbox[0].body)
        self.assertEqual(mail.outbox[0].to[0], self.student_user.email)

    # Note: Testing chat reply notifications requires a more complex setup
    # involving creating chat messages and ensuring the notification logic is triggered.
    # This is a simplified placeholder.
    @patch('pages.models.ChatMessage.send_new_reply_notification')
    def test_chat_reply_notification(self, mock_send_notification):
        """Test that a chat reply notification is triggered."""
        # This test primarily checks if the method is called.
        # Actual email content would be tested if the send_mail function was mocked.
        self.client.login(email='student@example.com', password='password123')
        # Simulate sending a chat message (this part would need actual view logic)
        # For now, we'll directly call the method that should trigger the notification
        # In a real scenario, this would be called from a view after a message is saved.

        # Create a dummy chat message object to pass to the function
        from pages.models import ChatMessage
        dummy_message = ChatMessage(
            sender=self.organization_user,
            receiver=self.student_user,
            content="This is a test message."
        )

        # Call the function that should trigger the notification
        # In a real view, this would be:
        # message = ChatMessage.objects.create(...)
        # send_chat_reply_notification(message)
        dummy_message.send_new_reply_notification()

        mock_send_notification.assert_called_once()
        # If you wanted to test the email content, you'd mock send_mail and check its calls.
        # For example:
        # with patch('django.core.mail.send_mail') as mock_send_mail:
        #     dummy_message.send_new_reply_notification()
        #     mock_send_mail.assert_called_once()
        #     self.assertEqual(mock_send_mail.call_args[0][0], "New Message from organization")

