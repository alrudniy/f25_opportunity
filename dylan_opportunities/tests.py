from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

class LoginTestCase(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpass123'
        User = get_user_model()
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.login_url = reverse('dylan_opportunities:login')

    def test_successful_login(self):
        """
        Test that a user with valid credentials can log in successfully.
        """
        response = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password,
        })
        # Successful login should redirect to LOGIN_REDIRECT_URL.
        self.assertRedirects(response, reverse('dylan_opportunities:home'), fetch_redirect_response=False)
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_failed_login_with_invalid_password(self):
        """
        Test that a user cannot log in with an invalid password.
        """
        response = self.client.post(self.login_url, {
            'username': self.username,
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct username and password.")
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_failed_login_with_nonexistent_username(self):
        """
        Test that a user cannot log in with a username that is not registered.
        """
        response = self.client.post(self.login_url, {
            'username': 'nonexistentuser',
            'password': 'anypassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct username and password.")
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_failed_login_with_empty_credentials(self):
        """
        Test that a user cannot log in with empty credentials.
        """
        response = self.client.post(self.login_url, {
            'username': '',
            'password': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")
        self.assertFalse('_auth_user_id' in self.client.session)
