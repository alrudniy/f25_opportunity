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
        self.company_user = User.objects.create_user(
            username='company@example.com',
            password='password',
            user_type='organization'
        )

    def test_non_company_user_is_redirected(self):
        """
        Verify that a logged-in non-company user is redirected from the company_about page.
        """
        self.client.login(username='student@example.com', password='password')
        response = self.client.get(reverse('company_about'))
        self.assertRedirects(response, reverse('screen1'))

    def test_company_user_can_access_page(self):
        """
        Verify that a logged-in company user can access the company_about page.
        """
        self.client.login(username='company@example.com', password='password')
        response = self.client.get(reverse('company_about'))
        self.assertEqual(response.status_code, 200)
