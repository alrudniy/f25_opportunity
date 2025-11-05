from django.test import TestCase

class RootUrlTests(TestCase):
    def test_root_url_returns_200(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)


