from django.test import SimpleTestCase
from django.urls import reverse

class BuggyViewTest(SimpleTestCase):
    """
    Tests for the intentionally buggy search view.
    These tests are designed to pass *after* the bugs are fixed,
    and they will fail with the original buggy code.
    """

    def test_buggy_search_no_query_param(self):
        """
        Bug 1: Verify the view doesn't crash if 'q' is missing.
        """
        response = self.client.get(reverse('buggy_search'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Buggy Search")

    def test_buggy_search_with_field_all(self):
        """
        Bug 2: Verify the view works correctly when field=All.
        """
        response = self.client.get(reverse('buggy_search') + '?q=ai&field=All')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "AI-Powered Chatbot")

    def test_buggy_search_with_query(self):
        """
        Bug 3: Verify the view returns results when querying description.
        """
        response = self.client.get(reverse('buggy_search') + '?q=city')
        self.assertEqual(response.status_code, 200)
        # In the fixed version, this should find one result.
        # In the buggy version, it raises a KeyError.
        self.assertContains(response, "Smart City Traffic Management")
