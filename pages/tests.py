from django.test import TestCase
from django.urls import reverse
from accounts.models import User

class CompanyAboutAccessTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a non-organization user (e.g., a student user)
        cls.student_user = User.objects.create_user(
            username='studentuser@example.com',
            email='studentuser@example.com',
            password='testpassword',
            user_type=User.UserType.STUDENT
        )
        # Create an organization user for comparison if needed in other tests
        cls.organization_user = User.objects.create_user(
            username='orguser@example.com',
            email='orguser@example.com',
            password='testpassword',
            user_type=User.UserType.ORGANIZATION
        )

    def test_non_organization_user_redirected_from_company_about(self):
        # Log in the student user
        self.client.login(username='studentuser@example.com', password='testpassword')
        
        # Attempt to access the company_about page
        response = self.client.get(reverse('company_about'))
        
        # Verify that the user is redirected to screen1
        self.assertRedirects(response, reverse('screen1'))

    def test_organization_user_can_access_company_about(self):
        # Log in the organization user
        self.client.login(username='orguser@example.com', password='testpassword')

        # Attempt to access the company_about page
        response = self.client.get(reverse('company_about'))

        # Verify that the user can access the page (status code 200)
        self.assertEqual(response.status_code, 200)
        # Optionally, check for some content specific to the company_about page
        self.assertContains(response, 'Mission')
        self.assertTemplateUsed(response, 'pages/company_about.html')
