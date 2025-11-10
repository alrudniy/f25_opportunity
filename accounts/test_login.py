from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class StudentLoginTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        # Creates a test user
        cls.test_user = User.objects.create_user(
            username='testuser', 
            password='testpassword'
        )

    def setUp(self):
        self.client = Client()
        # Original URL name, non-namespaced
        self.login_url = reverse('student_login') 

    # Test 1: Page Loads (Status 200)
    def test_1_login_page_loads(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    # Test 2: Successful Login
    def test_2_successful_login(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword'
        }, follow=True)
        # Check for successful redirection to 'welcome'
        self.assertRedirects(response, reverse('welcome'))

    # Test 3: Failed Login
    def test_3_failed_login(self):
        response = self.client.post(self.login_url, {
            'username': 'baduser',
            'password': 'badpassword'
        }, follow=True)
        # Check that it stays on the login page (status 200)
        self.assertEqual(response.status_code, 200)