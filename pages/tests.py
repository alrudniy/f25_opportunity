from django.test import SimpleTestCase
from django.urls import reverse


class PagesTestCase(SimpleTestCase):
    def test_welcome_page_loads(self):
        response = self.client.get(reverse("welcome"))
        self.assertEqual(response.status_code, 200)
