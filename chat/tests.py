from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Conversation, Message

User = get_user_model()

class ChatTests(TestCase):

    def setUp(self):
        self.student = User.objects.create_user(
            username='student@test.com',
            password='password123',
            user_type='student',
            first_name='Student',
            last_name='User'
        )
        self.organization = User.objects.create_user(
            username='org@test.com',
            password='password123',
            user_type='organization',
            first_name='Org',
            last_name='User'
        )
        self.client = Client()

    def test_start_conversation(self):
        self.client.login(username='student@test.com', password='password123')
        response = self.client.get(reverse('chat:start_conversation', args=[self.organization.id]))
        self.assertEqual(response.status_code, 302) # Redirect to conversation detail
        self.assertTrue(Conversation.objects.filter(participants=self.student).filter(participants=self.organization).exists())
        convo = Conversation.objects.filter(participants=self.student).filter(participants=self.organization).get()
        self.assertRedirects(response, reverse('chat:conversation_detail', args=[convo.id]))

    def test_send_message(self):
        self.client.login(username='student@test.com', password='password123')
        # Start conversation first
        self.client.get(reverse('chat:start_conversation', args=[self.organization.id]))
        convo = Conversation.objects.filter(participants=self.student).filter(participants=self.organization).get()

        # Send a message
        response = self.client.post(
            reverse('chat:conversation_detail', args=[convo.id]),
            {'content': 'Hello Organization!'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('chat:conversation_detail', args=[convo.id]))
        self.assertTrue(Message.objects.filter(conversation=convo, content='Hello Organization!').exists())
        message = Message.objects.get(conversation=convo)
        self.assertEqual(message.sender, self.student)

    def test_conversation_list_view(self):
        self.client.login(username='student@test.com', password='password123')
        self.client.get(reverse('chat:start_conversation', args=[self.organization.id]))
        
        response = self.client.get(reverse('chat:conversation_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Conversation with')
        self.assertQuerysetEqual(
            response.context['conversations'],
            Conversation.objects.filter(participants=self.student),
            transform=lambda x: x
        )
    
    def test_login_required_for_chat_views(self):
        # Conversation list
        response = self.client.get(reverse('chat:conversation_list'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('chat:conversation_list')}")
        
        # Start conversation
        response = self.client.get(reverse('chat:start_conversation', args=[self.organization.id]))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('chat:start_conversation', args=[self.organization.id])}")

        # Conversation detail (need a conversation to exist)
        convo = Conversation.objects.create()
        convo.participants.add(self.student, self.organization)
        response = self.client.get(reverse('chat:conversation_detail', args=[convo.id]))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('chat:conversation_detail', args=[convo.id])}")
