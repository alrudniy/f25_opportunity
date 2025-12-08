from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class CompanyAboutViewAccessTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.student_user = User.objects.create_user(
            username='student@test.com',
            email='student@test.com',
            password='testpassword',
            user_type='student',
            first_name='Student',
            last_name='User'
        )
        self.organization_user = User.objects.create_user(
            username='org@test.com',
            email='org@test.com',
            password='testpassword',
            user_type='organization',
            first_name='Org',
            last_name='User'
        )

    def test_student_user_redirected_from_company_about(self):
        """Verify non-company users are redirected from company_about page."""
        self.client.login(username='student@test.com', password='testpassword')
        response = self.client.get(reverse('company_about'))
        self.assertRedirects(response, reverse('screen1'))

    def test_organization_user_can_access_company_about(self):
        """Verify company users can access company_about page."""
        self.client.login(username='org@test.com', password='testpassword')
        response = self.client.get(reverse('company_about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/company_about.html')

    def test_unauthenticated_user_redirected_from_company_about(self):
        """Verify unauthenticated users are redirected from company_about page."""
        response = self.client.get(reverse('company_about'))
        expected_url = f"{reverse('login')}?next={reverse('company_about')}"
        self.assertRedirects(response, expected_url)
