from django.test import SimpleTestCase
from django.urls import reverse, resolve

class BuggyViewTests(SimpleTestCase):
    def test_buggy_view_url_resolves(self):
        # Checks that the URL name maps to a real view function
        resolver = resolve('/buggy/')
        self.assertEqual(resolver.view_name, 'buggy_search')
