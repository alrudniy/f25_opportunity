from django.test import TestCase
from django.urls import reverse
from accounts.models import User

class CompanyAboutPageTests(TestCase):

    def setUp(self):
        # Create an organization user for testing
        self.organization_user = User.objects.create_user(
            email='org@example.com',
            password='password123',
            user_type=User.UserType.ORGANIZATION,
            first_name='Test',
            last_name='Organization',
            username='test_org' # AbstractUser requires a username
        )
        self.organization_user.save() # Ensure display_name property is available

        # Log in the organization user
        self.client.login(email='org@example.com', password='password123')

    def test_company_about_url_resolves(self):
        url = reverse('company_about')
        self.assertEqual(url, '/pages/about/')

    def test_company_about_uses_correct_template(self):
        response = self.client.get(reverse('company_about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/company_about.html')

    def test_company_about_content_for_organization_user(self):
        response = self.client.get(reverse('company_about'))
        self.assertContains(response, f'About {self.organization_user.display_name}')
        self.assertContains(response, f'Email: {self.organization_user.email}')
        self.assertContains(response, 'Our Mission')
        self.assertContains(response, 'Problems We Solve')

    def test_company_home_links_to_company_about(self):
        # Access the company_home page
        # Note: Assuming 'dashboard' is the home for now, or you'd need a specific 'company_home' URL
        # For this test, we'll check the link existence in the general dashboard if applicable,
        # or mock a response for company_home if it has its own view.
        # Based on the template, company_home.html isn't directly wired via urlpatterns,
        # so we'll fetch it by rendering it if possible, or simulate its content.
        # For simplicity, we'll assume a path to company_home will eventually exist,
        # or test the direct rendering of the template with a dummy request if no view.

        # Since company_home.html is intended for logged-in organization, we'll simulate.
        # If there's a view that renders company_home, you'd call reverse() for that view.
        # For now, let's just assert the presence of the link in a generic logged-in context.
        # A more robust test would involve rendering the specific view that serves company_home.html

        # This test will require an actual view for company_home.
        # Assuming '/dashboard/' or another appropriate URL serves company_home.html for organization.
        # If 'company_home' has its own URL, please add it to pages/urls.py and update this test.
        response = self.client.get(reverse('dashboard')) # Assuming dashboard is the starting point
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'<a href="{reverse("company_about")}" class="btn btn-primary">Edit Profile</a>')
