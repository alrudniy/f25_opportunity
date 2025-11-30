from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class StudentProfileTests(TestCase):

    def setUp(self):
        """Set up test client and create a test user."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='teststudent',
            password='password123',
            first_name='Test',
            last_name='Student',
            university='Test University',
            class_year='2025',
            user_type=User.UserType.STUDENT
        )
        # Assuming 'login' is the name for your login view in accounts/urls.py
        # Assuming 'student_profile' is the name for your profile view in pages/urls.py or accounts/urls.py
        # You might need to adjust these URL names based on your actual project setup.
        self.login_url = reverse('login')
        self.profile_url = reverse('student_profile')

    def test_student_profile_view_accessible_to_logged_in_user(self):
        """Test that the student profile page is accessible to a logged-in student."""
        self.client.login(username='teststudent', password='password123')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        # Assuming your template for the student profile is named 'pages/student_profile.html'
        self.assertTemplateUsed(response, 'pages/student_profile.html')

    def test_student_profile_view_redirects_if_not_logged_in(self):
        """Test that the student profile page redirects to login if not logged in."""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)
        # Check if it redirects to the login page with the 'next' parameter set to the profile URL
        self.assertRedirects(response, f"{self.login_url}?next={self.profile_url}")

    def test_student_profile_page_displays_correct_info(self):
        """Test that the student profile page displays the correct user information."""
        self.client.login(username='teststudent', password='password123')
        response = self.client.get(self.profile_url)
        self.assertContains(response, 'Test')
        self.assertContains(response, 'Student')
        self.assertContains(response, 'Test University')
        self.assertContains(response, '2025')

    def test_student_profile_update_post_request(self):
        """Test updating student profile information via POST request."""
        self.client.login(username='teststudent', password='password123')
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Student',
            'university': 'New University',
            'class_year': '2026',
        }
        response = self.client.post(self.profile_url, update_data)

        # Check if the redirect is successful after update
        self.assertEqual(response.status_code, 302)
        # Check if it redirects back to the profile page after successful update
        self.assertRedirects(response, self.profile_url)

        # Refresh the user object from the database and check if data has been updated
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'Student')
        self.assertEqual(self.user.university, 'New University')
        self.assertEqual(self.user.class_year, '2026')

    def test_student_profile_update_with_invalid_data(self):
        """Test updating student profile with invalid data."""
        self.client.login(username='teststudent', password='password123')
        # Example of invalid data: assuming first_name is required and class_year has format validation
        invalid_data = {
            'first_name': '', # Assuming first name is required by the form
            'last_name': 'Student',
            'university': 'New University',
            'class_year': 'invalid_year', # Assuming class_year has validation (e.g., only digits)
        }
        response = self.client.post(self.profile_url, invalid_data)
        self.assertEqual(response.status_code, 200) # Should re-render the form with errors
        # You'll need to check for specific error messages based on your form's validation.
        # For example, if using Django's built-in validators:
        # self.assertContains(response, 'This field is required.')
        # self.assertContains(response, 'Enter a valid year.') # Example for class_year validation

    # Add more tests as needed, e.g., for administrator or organization profiles if applicable.
    # For example, testing that an organization user cannot access the student profile page,
    # or testing the specific validation rules for class_year.

