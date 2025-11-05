from django.test import TestCase
from django.urls import reverse


class DashboardPageTest(TestCase):
    def test_dashboard_page_view(self):
        """
        Tests that the dashboard page is accessible via name, returns a 200
        status code, and uses the correct template.
        """
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/dashboard.html')
