from django.test import SimpleTestCase


class FailingTest(SimpleTestCase):
    def test_failing_assertion(self):
        self.assertEqual(1, 2)
