from django.test import TestCase, Client
from django.urls import reverse, resolve
from accounts.models import User
from .views import company_about

class CompanyAboutPageTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testorg',
            email='contact@opportunity.com',
            password='password123',
            user_type=User.UserType.ORGANIZATION,
            first_name='Opportunity',
            last_name='App'
        )
        self.company_about_url = reverse('company_about')

    def test_company_about_view_requires_login(self):
        """
        Tests that an unauthenticated user is redirected to the login page.
        """
        response = self.client.get(self.company_about_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={self.company_about_url}")

    def test_company_about_view_for_logged_in_user(self):
        """
        Tests that a logged-in user can access the company about page and
        sees the correct content.
        """
        self.client.login(username='testorg', password='password123')
        response = self.client.get(self.company_about_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/company_about.html')
        self.assertContains(response, f"About {self.user.display_name}")
        self.assertContains(response, self.user.email)
        self.assertContains(response, "Our Mission")
        self.assertContains(response, "What We Solve")
        self.assertContains(response, "Contact Us")

    def test_company_about_url_resolves_to_correct_view(self):
        """
        Tests that the 'company_about' URL name resolves to the company_about view.
        """
        found = resolve(self.company_about_url)
        self.assertEqual(found.func, company_about)
