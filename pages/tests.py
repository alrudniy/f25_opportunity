from django.test import TestCase
from django.urls import reverse

class PagesTestCase(TestCase):
    def test_welcome_page_loads(self):
        """
        Simple test to verify that the welcome page can be loaded
        and returns HTTP 200 OK.
        """
        response = self.client.get(reverse('welcome'))
        self.assertEqual(response.status_code, 200)
