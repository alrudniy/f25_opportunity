from django.test import TestCase
from django.urls import reverse, NoReverseMatch

def _resolve_url(candidates, default_path):
    for name in candidates:
        try:
            return reverse(name)
        except NoReverseMatch:
            continue
    return default_path

class OpportunityAppSmokeTests(TestCase):
    """
    Smoke tests aligned with your current templates.
    - Welcome: checks page loads + key text
    - Login: checks header/button text and presence of Create account link
    - Forgot password: tries common routes; if 404, skip (not configured yet)
    - Create account: checks header and field labels with exact casing
    """

    def test_welcome_page_loads(self):
        url = _resolve_url(
            ["welcome", "pages:welcome", "home", "pages:home"],
            "/",
        )
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Welcome")
        self.assertContains(resp, "Student")
        self.assertContains(resp, "Organization")

    def test_login_page_text_and_links(self):
        url = _resolve_url(
            ["login", "accounts:login"],
            "/accounts/login/",
        )
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        # Exact casing from your HTML
        self.assertContains(resp, "Sign in")
        self.assertContains(resp, "Email")
        self.assertContains(resp, "Password")
        # You currently have a "Create account" link
        self.assertContains(resp, "Create account")

    def test_forgot_password_page_if_configured(self):
        # Try a few common names/paths
        url = _resolve_url(
            ["password_reset", "accounts:password_reset"],
            "/accounts/password_reset/",
        )
        resp = self.client.get(url)
        if resp.status_code == 404:
            self.skipTest("Password reset page not configured yet")
        else:
            self.assertEqual(resp.status_code, 200)
            # Relaxed checks in case text differs later; update as you build it
            self.assertContains(resp, "password", status_code=200)

    def test_create_account_page_inputs(self):
        url = _resolve_url(
            ["signup", "register", "accounts:signup", "accounts:register"],
            "/accounts/register/",
        )
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Create Account")
        self.assertContains(resp, "Email")
        self.assertContains(resp, "Password")
        # Exact label from your HTML is "Confirm Password"
        self.assertContains(resp, "Confirm Password")