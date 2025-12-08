from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User

class CompanyAboutViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.student_user = User.objects.create_user(
            email='student@test.com',
            password='password123',
            user_type=User.UserType.STUDENT
        )
        self.organization_user = User.objects.create_user(
            email='org@test.com',
            password='password123',
            user_type=User.UserType.ORGANIZATION
        )
        self.company_about_url = reverse('company_about')
        self.screen1_url = reverse('screen1')

    def test_non_organization_user_is_redirected(self):
        """
        Verify that a logged-in user who is not an 'organization'
        is redirected from the company_about page to screen1.
        """
        self.client.login(email='student@test.com', password='password123')
        response = self.client.get(self.company_about_url)
        self.assertRedirects(response, self.screen1_url)

    def test_organization_user_can_access_page(self):
        """
        Verify that a logged-in 'organization' user can access
        the company_about page.
        """
        self.client.login(email='org@test.com', password='password123')
        response = self.client.get(self.company_about_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/company_about.html')
