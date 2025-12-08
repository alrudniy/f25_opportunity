from django.test import TestCase
from django.urls import reverse

from accounts.models import User


class CompanyHomeAccessTest(TestCase):
    def setUp(self):
        """Set up a non-company user for testing."""
        self.student_user = User.objects.create_user(
            username='studentuser',
            email='student@example.com',
            password='password123',
            user_type=User.UserType.STUDENT
        )

    def test_non_company_user_redirected(self):
        """
        Verify that a logged-in user who is not a company user is redirected
        from the company_home page to screen1.
        """
        self.client.login(username='studentuser', password='password123')
        response = self.client.get(reverse('company_home'))
        self.assertRedirects(response, reverse('screen1'))
