from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

# Get the custom user model (if you have one, or it defaults to the standard User)
User = get_user_model()

class StudentLoginTest(TestCase):
    # This method runs before every test to set up the environment
    def setUp(self):
        # 1. Initialize the Django test client
        self.client = Client()
        
        # 2. Create a test user in the database.
        # This user is created and destroyed *only* for this test run.
        self.test_user = User.objects.create_user(
            username='student_test',
            email='test@student.com',
            password='Password123!'
        )
        
        # 3. Define the login URL name used in your project's urls.py
        # You may need to change 'login' if your URL name is different
        self.login_url = reverse('login')
        
        # 4. Define the target URL after successful login (e.g., the student dashboard)
        # You may need to change 'dashboard' if your URL name is different
        self.redirect_url = reverse('dashboard') 

    def test_successful_student_login(self):
        """
        Tests that a user can successfully log in with valid credentials.
        """
        # The data that mimics a user typing into the login form fields
        login_credentials = {
            'username': 'student_test',
            'password': 'Password123!', 
        }
        
        # 1. Simulate a POST request to the login URL.
        # follow=True tells the client to follow the 302 redirect all the way to the final 200 page.
        response = self.client.post(self.login_url, login_credentials, follow=True)

        # 2. ASSERTION 1: Check the final status code
        # We expect the final page (dashboard) to load successfully (HTTP 200)
        self.assertEqual(response.status_code, 200) 
        
        # 3. ASSERTION 2: Check if the client session is now authenticated
        self.assertTrue(response.context['user'].is_authenticated)

        # 4. ASSERTION 3: Check that the user landed on the correct template
        # You may need to change 'dashboard.html' to your actual template file name
        self.assertTemplateUsed(response, 'opportunity/dashboard.html')