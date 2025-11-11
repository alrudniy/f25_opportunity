from django.test import TestCase

class BuggyViewTests(TestCase):
    def test_bug_1_repro_on_buggy(self):
        # Expect the AttributeError from BUG 1 (None.strip())
        with self.assertRaises(AttributeError):
            self.client.get("/buggy/")  # no ?q= -> triggers None.strip()

    def test_fixed_no_crash(self):
        # Fixed view should render without q
        resp = self.client.get("/buggy_fixed/")
        self.assertEqual(resp.status_code, 200)

    def test_fixed_all_filter_logic(self):
        # BUG 2 fixed: using == instead of "is"
        resp = self.client.get("/buggy_fixed/", {"q": "ai", "field": "All"})
        self.assertEqual(resp.status_code, 200)
        # Page should include something from the AI item; "AI" is enough to sanity-check
        self.assertContains(resp, "AI")

    def test_fixed_description_keyerror(self):
        # BUG 3 fixed: correct 'description' key
        resp = self.client.get("/buggy_fixed/", {"q": "city"})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "City")
