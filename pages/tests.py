from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User # Assuming your custom User model is in accounts.models

class CompanyAboutViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.organization_user = User.objects.create_user(
            email='org@example.com',
            password='testpassword',
            user_type=User.UserType.ORGANIZATION,
            first_name='Org',
            last_name='User'
        )
        self.student_user = User.objects.create_user(
            email='student@example.com',
            password='testpassword',
            user_type=User.UserType.STUDENT,
            first_name='Student',
            last_name='User'
        )
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='testpassword',
            first_name='Admin',
            last_name='User'
        )
        self.company_about_url = reverse('company_about')
        self.login_url = reverse('login')
        self.screen1_url = reverse('screen1') # Add screen1_url for the redirect check

    def test_company_about_redirects_if_not_logged_in(self):
        response = self.client.get(self.company_about_url)
        self.assertRedirects(response, f'{self.login_url}?next={self.company_about_url}')

    def test_company_about_redirects_student_user(self):
        self.client.login(email='student@example.com', password='testpassword')
        response = self.client.get(self.company_about_url)
        self.assertRedirects(response, self.screen1_url)

    def test_company_about_redirects_admin_user(self):
        self.client.login(email='admin@example.com', password='testpassword')
        response = self.client.get(self.company_about_url)
        self.assertRedirects(response, self.screen1_url)

    def test_company_about_loads_for_organization_user(self):
        self.client.login(email='org@example.com', password='testpassword')
        response = self.client.get(self.company_about_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/company_about.html')

    def test_company_about_displays_correct_content_for_organization(self):
        self.client.login(email='org@example.com', password='testpassword')
        response = self.client.get(self.company_about_url)

        self.assertContains(response, self.organization_user.display_name)
        self.assertContains(response, "Our mission is to empower the next generation of talent by connecting them with meaningful opportunities.")
        self.assertContains(response, "We help companies overcome recruitment challenges by streamlining the process of finding and engaging with skilled students and graduates.")
        self.assertContains(response, self.organization_user.email)
