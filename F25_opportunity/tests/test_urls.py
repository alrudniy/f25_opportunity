from django.test import SimpleTestCase


class SimpleTest(SimpleTestCase):
    def test_simple_assertion(self):
        self.assertEqual(1, 2)
