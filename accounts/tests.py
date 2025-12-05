from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class LogoutTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.logout_url = reverse('logout')
        self.welcome_url = reverse('welcome')

        # Create a test user for login
        self.username = 'testuser@example.com'
        self.password = 'testpassword123'
        self.user = User.objects.create_user(
            username=self.username,
            email=self.username,
            password=self.password,
            user_type='student'
        )

    def test_post_only_logout_redirects_to_welcome_and_clears_session(self):
        # 1. Log in the client
        login_success = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login_success, "Client should be able to log in successfully")
        self.assertTrue('_auth_user_id' in self.client.session, "User ID should be in session after login")

        # 2. Simulate a POST request to the logout URL and follow redirects
        response = self.client.post(self.logout_url, follow=True)

        # 3. Verify a POST request was made (implicit with client.post)
        #    and verify successful logout and redirection to welcome page
        self.assertEqual(response.status_code, 200) # Final status after following redirects
        self.assertRedirects(response, self.welcome_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'pages/welcome.html')

        # 4. Verify the session is cleared (user is logged out)
        self.assertFalse('_auth_user_id' in self.client.session, "User ID should not be in session after logout")
        self.assertIsNone(self.client.session.get('_auth_user_id'), "User ID should be None in session after logout")
        self.assertFalse(response.context['user'].is_authenticated, "User should not be authenticated in the response context")

        # 5. Verify the user ends up on the Welcome page
        self.assertEqual(response.request['PATH_INFO'], self.welcome_url)
        self.assertContains(response, "Welcome", html=True) # Assuming "Welcome" text exists on welcome.html

        # 6. Verify no authenticated navigation visible on the Welcome page.
        #    This assumes 'Dashboard' or 'Logout' links are specific to authenticated users,
        #    and 'Login', 'Register' are for guest users on the welcome page.
        self.assertNotContains(response, 'Dashboard', html=True)
        self.assertNotContains(response, 'Logout', html=True)
        self.assertContains(response, 'Login', html=True)
        self.assertContains(response, 'Register', html=True)


    def test_get_request_to_logout_is_not_allowed(self):
        # Log in the client first to ensure a session exists
        self.client.login(username=self.username, password=self.password)
        self.assertTrue('_auth_user_id' in self.client.session)

        # Attempt to access logout with GET
        response = self.client.get(self.logout_url)

        # Verify that a GET request is not allowed (HTTP 405 Method Not Allowed)
        self.assertEqual(response.status_code, 405)
        self.assertContains(response, 'Method Not Allowed', status_code=405)

        # Ensure user is still logged in after a failed GET logout attempt
        self.assertTrue('_auth_user_id' in self.client.session, "User should remain logged in after a GET logout attempt")
        self.assertIsNotNone(self.client.session.get('_auth_user_id'), "User ID should still be present in session")
