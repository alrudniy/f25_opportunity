from django.test import TestCase
from django.urls import reverse
from accounts.models import User


class HelloStudentPageTest(TestCase):
    def setUp(self):
        """Set up a student user for testing."""
        self.student_user = User.objects.create_user(
            username='teststudent',
            email='teststudent@example.com',
            password='password123',
            first_name='Test',
            last_name='Student',
            user_type='student'
        )

    def test_hello_student_page_content_and_links(self):
        """
        Test that the Hello Student page displays correctly for a logged-in student,
        including the header, buttons, and clickable links.
        """
        # Log in the student
        self.client.login(username='teststudent', password='password123')

        # Access the hello_student page
        url = reverse('hello_student')
        response = self.client.get(url)

        # Verify page loads successfully
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/hello_student.html')

        # Verify that the header displays the correct student name
        self.assertContains(response, f"<h1>Hello {self.student_user.display_name}</h1>", html=True)

        # Check that all five action buttons are present
        buttons = [
            'Your Applications',
            'Your Profile',
            'Peer Activities',
            'Post Your Experience',
            'Find New Opportunities',
        ]
        for button_text in buttons:
            self.assertContains(response, button_text)

        # Confirm that buttons with links are clickable and lead to the correct page
        response_achievements = self.client.get(reverse('student_achievements'))
        self.assertEqual(response_achievements.status_code, 200)

        response_screen1 = self.client.get(reverse('screen1'))
        self.assertEqual(response_screen1.status_code, 200)
