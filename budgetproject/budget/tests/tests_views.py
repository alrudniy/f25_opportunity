from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

# Get the custom user model (if you're using one, otherwise it defaults to User)
User = get_user_model()

class StudentLoginTest(TestCase):
    # This setup method runs BEFORE every single test case
    def setUp(self):
        # 1. Initialize the test client
        self.client = Client()
        
        # 2. Create a test user for the login attempt
        self.test_user = User.objects.create_user(
            username='student_test',
            email='test@student.com',
            password='Password123!'
        )
        
        # 3. Define the login URL (adjust 'login' if your URL name is different)
        self.login_url = reverse('login')
        
        # 4. Define the URL where a user is redirected after a successful login (e.g., dashboard)
        self.redirect_url = reverse('dashboard') 

    def test_student_login_success(self):
        """
        Tests that a user can successfully log in with valid credentials.
        """
        # Data dictionary to simulate the form submission
        login_credentials = {
            'username': 'student_test',
            'password': 'Password123!'
        }
        
        # 1. Simulate a POST request to the login URL
        response = self.client.post(self.login_url, login_credentials, follow=True)

        # 2. ASSERTION 1: Check the final status code
        # A successful login typically redirects (302) to the dashboard (200)
        # 'follow=True' means the response is the final 200 page.
        self.assertEqual(response.status_code, 200) 
        
        # 3. ASSERTION 2: Check if the client is now authenticated
        self.assertTrue(response.context['user'].is_authenticated)

        # 4. ASSERTION 3: Check that the user landed on the expected page
        self.assertTemplateUsed(response, 'dashboard.html') # Check the template name
        # OR: self.assertRedirects(response, self.redirect_url) if follow=False

# NOTE: Replace 'login', 'dashboard', and 'dashboard.html' with the actual values in your project's urls.py and templates.