from django.test import TestCase
from django.urls import reverse

class PagesTestCase(TestCase):
    def test_welcome_page_loads(self):
        response = self.client.get(reverse('welcome'))
        self.assertEqual(response.status_code, 200)

    def test_contact_page_loads(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)

    def test_screen1_page_loads_for_authenticated_user(self):
        # Create a user for testing
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.create_user(username='testuser', password='password', user_type='student')
        self.client.login(username='testuser', password='password')
        
        response = self.client.get(reverse('screen1'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello testuser (Student)")

    def test_screen1_page_redirects_unauthenticated_user(self):
        response = self.client.get(reverse('screen1'))
        self.assertEqual(response.status_code, 302) # Redirects to login
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('screen1')}")

    def test_screen2_page_loads_for_authenticated_user(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.create_user(username='testuser', password='password', user_type='organization')
        self.client.login(username='testuser', password='password')
        
        response = self.client.get(reverse('screen2'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello testuser (Organization)")

    def test_screen2_page_redirects_unauthenticated_user(self):
        response = self.client.get(reverse('screen2'))
        self.assertEqual(response.status_code, 302) # Redirects to login
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('screen2')}")

    def test_screen3_page_loads_for_authenticated_user(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.create_user(username='testuser', password='password', user_type='administrator')
        self.client.login(username='testuser', password='password')
        
        response = self.client.get(reverse('screen3'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello testuser (Administrator)")

    def test_screen3_page_redirects_unauthenticated_user(self):
        response = self.client.get(reverse('screen3'))
        self.assertEqual(response.status_code, 302) # Redirects to login
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('screen3')}")
