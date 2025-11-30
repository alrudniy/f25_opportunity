from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from django.core import mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator

class PasswordResetFlowTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_model = get_user_model()
        self.email = "student_oppo@drew.edu"
        self.password = "a_very_secure_password"
        self.user = self.user_model.objects.create_user(email=self.email, password=self.password)

    def test_forgot_password_flow(self):
        # 1. Load the login page and confirm "Forgot password" link
        login_url = reverse('login')
        response = self.client.get(login_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Forgot password?')

        # 2. POST to the password_reset view
        password_reset_url = reverse('password_reset')
        response = self.client.post(password_reset_url, {'email': self.email})

        # 3. Assert that a reset email is sent
        self.assertEqual(len(mail.outbox), 1)
        reset_email = mail.outbox[0]
        self.assertEqual(reset_email.to[0], self.email)
        self.assertIn('Password reset', reset_email.subject)

        # 4. Extract the reset URL from the email
        # The email body contains a link like:
        # "You're receiving this e-mail because you or someone else,
        # has requested a password reset for your account.
        #
        # To reset your password, visit the following URL:
        # http://localhost:8000/password-reset/done/
        #
        # If you did not request this, please ignore this email.
        #
        # Thanks,
        # The Django sites admin"
        # We need to find the actual reset link within the email body.
        # Django's default password reset email template includes the URL.
        # We can parse the email body to find it.
        # A more robust way is to use the token generator and user to construct the URL.

        # Construct the expected reset URL
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        expected_reset_confirm_url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})

        # Check if the email contains the correct URL
        self.assertIn(expected_reset_confirm_url, reset_email.body)

        # 5. Open the reset URL and submit a new password
        reset_confirm_url = f"{expected_reset_confirm_url}" # Assuming the email body contains the full URL or relative path
        response = self.client.get(reset_confirm_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New password')

        new_password = "a_new_and_even_better_password"
        response = self.client.post(reset_confirm_url, {
            'password1': new_password,
            'password2': new_password,
        })

        # 6. Confirm that the reset completes and user can log in with the new password
        password_reset_complete_url = reverse('password_reset_complete')
        self.assertRedirects(response, password_reset_complete_url)

        # Verify the user can log in with the new password
        login_response = self.client.post(login_url, {'email': self.email, 'password': new_password})
        self.assertRedirects(login_response, reverse('screen1'))
        self.assertIn('_auth_user_id', self.client.session)
