from django.test import SimpleTestCase
from django.urls import reverse, resolve

from .views import dashboard


class DashboardPageTest(SimpleTestCase):
    def test_dashboard_url_resolves(self):
        """
        Tests that the URL for the dashboard resolves to the correct view.
        """
        url = reverse('dashboard')
        self.assertEqual(url, '/dashboard/')
        resolver = resolve(url)
        self.assertEqual(resolver.func, dashboard)
