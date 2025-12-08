from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User


class CompanyAboutAccessTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.student_user = User.objects.create_user(
            username='student@example.com',
            password='password',
            user_type='student'
        )

    def test_non_company_user_is_redirected(self):
        """
        Verify that a logged-in non-company user is redirected from the company_about page.
        """
        self.client.login(username='student@example.com', password='password')
        response = self.client.get(reverse('company_about'))
        self.assertRedirects(response, reverse('screen1'))
