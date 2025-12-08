from django.test import TestCase
from django.urls import reverse
from accounts.models import User

class CompanyAboutAccessTest(TestCase):
    def setUp(self):
        # Create a non-company user (e.g., a student user)
        self.student_user = User.objects.create_user(
            username='studentuser',
            email='student@example.com',
            password='testpassword',
            user_type=User.UserType.STUDENT
        )
        self.student_user.display_name = 'Student User'
        self.student_user.save()

    def test_non_company_user_access_company_about(self):
        # Log in the student user
        self.client.login(username='studentuser', password='testpassword')

        # Attempt to access the company_about page
        response = self.client.get(reverse('company_about'))

        # Assert that the user is redirected (status code 302)
        self.assertEqual(response.status_code, 302)

        # Assert that the user is redirected to the screen1 page (LOGIN_REDIRECT_URL)
        self.assertRedirects(response, reverse('screen1'))
from django.test import TestCase
from django.urls import reverse
from accounts.models import User

class CompanyAboutAccessTest(TestCase):
    def setUp(self):
        # Create a non-company user (e.g., a student user)
        self.student_user = User.objects.create_user(
            username='studentuser',
            email='student@example.com',
            password='testpassword',
            user_type=User.UserType.STUDENT
        )
        self.student_user.display_name = 'Student User'
        self.student_user.save()

    def test_non_company_user_access_company_about(self):
        # Log in the student user
        self.client.login(username='studentuser', password='testpassword')

        # Attempt to access the company_about page
        response = self.client.get(reverse('company_about'))

        # Assert that the user is redirected (status code 302)
        self.assertEqual(response.status_code, 302)

        # Assert that the user is redirected to the screen1 page (LOGIN_REDIRECT_URL)
        self.assertRedirects(response, reverse('screen1'))
