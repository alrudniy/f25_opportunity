from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import UserSettings

User = get_user_model()

class UserSettingsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = Client()
        self.client.login(username='testuser', password='password')
        self.settings_url = reverse('user_settings:settings')

    def test_settings_page_loads(self):
        response = self.client.get(self.settings_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_settings/settings.html')

    def test_user_settings_created_automatically(self):
        self.assertTrue(UserSettings.objects.filter(user=self.user).exists())
        self.assertIsNotNone(self.user.settings)

    def test_settings_are_updated_and_persist(self):
        # Check initial default values
        self.assertTrue(self.user.settings.receive_updates)
        self.assertTrue(self.user.settings.public_experience)
        self.assertTrue(self.user.settings.notifications_on)
        self.assertEqual(self.user.settings.theme, 'auto')

        # Post new settings
        new_settings = {
            'receive_updates': 'off', # checkboxes send 'on' or nothing
            'public_experience': 'off',
            'notifications_on': 'off',
            'theme': 'dark',
        }
        # A real form submission from a browser for unchecked boxes would not include the key.
        # The Django test client requires us to be explicit.
        # Let's post data that mimics a form with unchecked boxes.
        response = self.client.post(self.settings_url, {'theme': 'dark'})
        self.assertEqual(response.status_code, 302)
        
        self.user.settings.refresh_from_db()

        self.assertFalse(self.user.settings.receive_updates)
        self.assertFalse(self.user.settings.public_experience)
        self.assertFalse(self.user.settings.notifications_on)
        self.assertEqual(self.user.settings.theme, 'dark')

        # Test changing them back to True
        response = self.client.post(self.settings_url, {
            'receive_updates': 'on',
            'public_experience': 'on',
            'notifications_on': 'on',
            'theme': 'light'
        })
        self.assertEqual(response.status_code, 302)

        self.user.settings.refresh_from_db()
        self.assertTrue(self.user.settings.receive_updates)
        self.assertTrue(self.user.settings.public_experience)
        self.assertTrue(self.user.settings.notifications_on)
        self.assertEqual(self.user.settings.theme, 'light')
