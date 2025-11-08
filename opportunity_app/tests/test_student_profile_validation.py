from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class StudentProfileValidationTest(TestCase):
    """Simplified tests to ensure invalid inputs do not crash the student profile page."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        self.profile_url = reverse('edit_profile_student')
        self.valid_data = {
            'first_name': 'Valid',
            'last_name': 'Name',
            'class_year': '2025',
            'university': 'Valid University',
        }

    def post_and_check(self, data):
        """Helper to post data and ensure no server error occurs."""
        response = self.client.post(self.profile_url, data)
        # Ensure system doesn't crash (200 or redirect 302 are fine)
        self.assertIn(response.status_code, [200, 302])

    def test_first_name_field_validation(self):
        invalid_inputs = ['@#$', '12345', '', '<script>alert(1)</script>', 'a' * 151]
        for case in invalid_inputs:
            with self.subTest(case=case):
                data = self.valid_data.copy()
                data['first_name'] = case
                self.post_and_check(data)

    def test_class_year_field_validation(self):
        invalid_inputs = ['abcd', '!@#$', '', '2025.5', '202520252025']
        for case in invalid_inputs:
            with self.subTest(case=case):
                data = self.valid_data.copy()
                data['class_year'] = case
                self.post_and_check(data)

    def test_university_field_validation(self):
        invalid_inputs = ['', 'a' * 201, '<script>evil()</script>', 'Uni@#$', '123']
        for case in invalid_inputs:
            with self.subTest(case=case):
                data = self.valid_data.copy()
                data['university'] = case
                self.post_and_check(data)