from django.test import SimpleTestCase
from django.urls import resolve, reverse


class UrlTests(SimpleTestCase):
    def test_admin_url_resolves(self):
        url = reverse("admin:index")
        self.assertEqual(resolve(url).view_name, "admin:index")
