from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

# We will need to import Student and Organization models/profiles.
# For example: from users.models import Student, Organization

User = get_user_model()

class ChatTestCase(TestCase):
    def setUp(self):
        # This setup will need to be adjusted based on your actual user models.
        # I am assuming you have a way to create a student user and an organization user.
        self.student_user = User.objects.create_user(username='student', password='password')
        # self.student_profile = Student.objects.create(user=self.student_user)

        self.org_user = User.objects.create_user(username='organization', password='password')
        # self.org_profile = Organization.objects.create(user=self.org_user)

        self.student_client = Client()
        self.student_client.login(username='student', password='password')

        self.org_client = Client()
        self.org_client.login(username='organization', password='password')

    def test_student_starts_conversation_and_sends_message(self):
        # Student starts a conversation with the organization
        start_conv_url = reverse('chat:start_conversation', args=[self.org_user.id])
        response = self.student_client.get(start_conv_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/conversation_detail.html')
        
        # There should be one conversation now
        self.assertEqual(self.student_user.conversations.count(), 1)
        conversation = self.student_user.conversations.first()
        self.assertIn(self.org_user, conversation.participants.all())

        # Student sends a message
        conv_detail_url = reverse('chat:conversation_detail', args=[conversation.id])
        message_content = "Hello, I am interested in your opportunity."
        response = self.student_client.post(conv_detail_url, {'content': message_content}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, message_content)
        self.assertEqual(conversation.messages.count(), 1)
        self.assertEqual(conversation.messages.first().content, message_content)
        self.assertEqual(conversation.messages.first().sender, self.student_user)

        # Organization logs in and sees the message
        response = self.org_client.get(conv_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, message_content)

        # Organization replies
        reply_content = "Thank you for your interest. We will get back to you soon."
        response = self.org_client.post(conv_detail_url, {'content': reply_content}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reply_content)
        self.assertEqual(conversation.messages.count(), 2)

        # Student sees the reply
        response = self.student_client.get(conv_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reply_content)
