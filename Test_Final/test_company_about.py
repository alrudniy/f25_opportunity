from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class CompanyAboutAccessTest(TestCase):

    def setUp(self):
        """Set up a non-company user for testing."""
        self.non_company_user = User.objects.create_user(
            username='university.user',
            password='password123',
            user_type='university'
        )
        self.client.login(username='university.user', password='password123')

    def test_non_company_user_redirected_from_company_about(self):
        """
        Verify that a logged-in, non-company user is redirected from the 
        company_about page to screen1.
        """
        response = self.client.get(reverse('company_about'))
        self.assertRedirects(response, reverse('screen1'))
