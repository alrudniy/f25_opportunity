from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class StudentProfileValidationTest(TestCase):

    def setUp(self):
        """Set up a user and log them in."""
        self.user = User.objects.create_user(username='teststudent', password='password123')
        self.client.login(username='teststudent', password='password123')
        # We assume the user has a student profile instance created upon user creation.
        # We assume 'student_profile' is the URL name for the profile page view.
        # This view should handle both GET and POST for displaying and updating the profile.
        self.profile_url = reverse('student_profile')
        self.valid_data = {
            'name': 'Valid Name',
            'class_year': '2025',
            'school': 'Valid University',
        }

    def test_name_field_validation(self):
        """Test validation for the 'name' field."""
        invalid_names = {
            "special_chars": 'Name With Special Chars@#$',
            "numbers": 'NameWithNumbers123',
            "empty": '',
            "code_injection": '<script>alert("xss")</script>',
            "long_text": 'a' * 151,  # Assuming max_length=150
        }
        for test_case, name in invalid_names.items():
            with self.subTest(case=test_case):
                data = self.valid_data.copy()
                data['name'] = name
                response = self.client.post(self.profile_url, data)
                self.assertEqual(response.status_code, 200)
                self.assertIn('name', response.context['form'].errors)

    def test_class_year_field_validation(self):
        """Test validation for the 'class_year' field."""
        invalid_years = {
            "non_numeric": 'not_a_year',
            "special_chars": '2025!',
            "empty": '',
            "float": '2025.5',
            "too_long": '12345',  # Assuming a 4-digit year
            "code_injection": '<script>alert("xss")</script>',
        }
        for test_case, year in invalid_years.items():
            with self.subTest(case=test_case):
                data = self.valid_data.copy()
                data['class_year'] = year
                response = self.client.post(self.profile_url, data)
                self.assertEqual(response.status_code, 200)
                self.assertIn('class_year', response.context['form'].errors)

    def test_school_field_validation(self):
        """Test validation for the 'school' field."""
        invalid_schools = {
            "empty": '',
            "long_text": 'a' * 201,  # Assuming max_length=200
            "special_chars": 'School With Special Chars@#$',
            "code_injection": '<script>alert("xss")</script>',
        }
        for test_case, school in invalid_schools.items():
            with self.subTest(case=test_case):
                data = self.valid_data.copy()
                data['school'] = school
                response = self.client.post(self.profile_url, data)
                self.assertEqual(response.status_code, 200)
                self.assertIn('school', response.context['form'].errors)
