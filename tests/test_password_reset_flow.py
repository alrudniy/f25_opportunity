from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail
import re


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class PasswordResetFlowTests(TestCase):
    def setUp(self):
        self.client = Client()
        User = get_user_model()
        self.email = "student_oppo@drew.edu"
        self.password = "a_very_secure_password"

        # If your custom user model uses email as USERNAME_FIELD, this is enough
        self.user = User.objects.create_user(
            email=self.email,
            password=self.password,
        )

    def test_forgot_password_flow(self):
        # 1. Load the login page and confirm "Forgot password" link
        login_url = reverse("login")
        response = self.client.get(login_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Forgot password")

        # 2. POST to the password_reset view
        password_reset_url = reverse("password_reset")
        response = self.client.post(password_reset_url, {"email": self.email})
        # password_reset usually redirects to the "done" page
        self.assertEqual(response.status_code, 302)

        # 3. Assert that a reset email is sent
        self.assertEqual(len(mail.outbox), 1)
        reset_email = mail.outbox[0]
        self.assertIn(self.email, reset_email.to)

        # 4. Extract the reset URL from the email body
        body = reset_email.body
        match = re.search(r"http://testserver[^\s]+", body)
        self.assertIsNotNone(match, "No reset URL found in email body")
        reset_url = match.group(0)

        # 5. Open the reset URL and submit a new password
        response = self.client.get(reset_url)
        self.assertEqual(response.status_code, 200)

        new_password = "a_new_and_even_better_password"
        response = self.client.post(
            reset_url,
            {
                "new_password1": new_password,
                "new_password2": new_password,
            },
        )

        password_reset_complete_url = reverse("password_reset_complete")
        self.assertRedirects(response, password_reset_complete_url)

        # 6. Verify the user can log in with the new password
        login_response = self.client.post(
            login_url,
            {
                "email": self.email,
                "password": new_password,
            },
        )
        self.assertEqual(login_response.status_code, 302)
        self.assertRedirects(login_response, reverse("screen1"))
        self.assertIn("_auth_user_id", self.client.session)
