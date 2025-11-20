from django.test import SimpleTestCase
from django.urls import reverse


class PagesTestCase(SimpleTestCase):
    def test_welcome_page_loads(self):
        response = self.client.get(reverse("welcome"))
        self.assertEqual(response.status_code, 200)

    def test_contact_page_loads(self):
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)

    def test_screen1_page_redirects_unauthenticated(self):
        response = self.client.get(reverse("screen1"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('screen1')}")

    def test_screen2_page_redirects_unauthenticated(self):
        response = self.client.get(reverse("screen2"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('screen2')}")

    def test_screen3_page_redirects_unauthenticated(self):
        response = self.client.get(reverse("screen3"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('screen3')}")
