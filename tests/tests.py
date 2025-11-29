from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from pages.models import FindOpportunity
from datetime import date, timedelta

User = get_user_model()


class FindOpportunitiesTestCase(TestCase):
    """Test suite with 10 essential tests"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()

        # Create student user
        self.student = User.objects.create_user(
            username='student_oppo@drew.edu',
            email='student_oppo@drew.edu',
            password='1Opportunity!',
            user_type='student',
        )

        # Create organization
        self.org = User.objects.create_user(
            username='org_oppo@drew.edu',
            email='org_oppo@drew.edu',
            password='1Opportunity!',
            user_type='organization',
        )

        # Create 3 volunteer opportunities
        FindOpportunity.objects.create(
            title='Beach Cleanup',
            description='Clean beaches',
            opportunity_type='volunteer',
            organization=self.org,
            city='San Francisco',
            state='California',
            is_remote=False,
            status='published'
        )

        FindOpportunity.objects.create(
            title='Virtual Tutor',
            description='Tutor online',
            opportunity_type='volunteer',
            organization=self.org,
            is_remote=True,
            status='published'
        )

        FindOpportunity.objects.create(
            title='Garden Helper',
            description='Help in garden',
            opportunity_type='volunteer',
            organization=self.org,
            city='Oakland',
            state='California',
            is_remote=False,
            status='published'
        )

        # Create 2 internships
        FindOpportunity.objects.create(
            title='Software Intern',
            description='Build apps',
            opportunity_type='internship',
            organization=self.org,
            city='San Francisco',
            state='California',
            is_remote=False,
            status='published'
        )

        FindOpportunity.objects.create(
            title='Marketing Intern',
            description='Social media',
            opportunity_type='internship',
            organization=self.org,
            is_remote=True,
            status='published'
        )

        self.client.login(email='student_oppo@drew.edu', password='1Opportunity!')

    def test_page_loads(self):
        """Test page loads successfully"""
        response = self.client.get(reverse('screen1'))
        self.assertEqual(response.status_code, 200)

    def test_all_opportunities_show(self):
        """Test all 5 published opportunities display"""
        response = self.client.get(reverse('screen1'))
        self.assertEqual(response.context['total_count'], 5)

    def test_filter_volunteer(self):
        """Test filter by volunteer type"""
        response = self.client.get(reverse('screen1'), {'opportunity_type': 'volunteer'})
        self.assertEqual(response.context['total_count'], 3)

    def test_filter_internship(self):
        """Test filter by internship type"""
        response = self.client.get(reverse('screen1'), {'opportunity_type': 'internship'})
        self.assertEqual(response.context['total_count'], 2)

    def test_filter_remote(self):
        """Test filter by remote location"""
        response = self.client.get(reverse('screen1'), {'location_type': 'remote'})
        self.assertEqual(response.context['total_count'], 2)

    def test_filter_in_person(self):
        """Test filter by in-person location"""
        response = self.client.get(reverse('screen1'), {'location_type': 'in_person'})
        self.assertEqual(response.context['total_count'], 3)

    def test_filter_city(self):
        """Test filter by city"""
        response = self.client.get(reverse('screen1'), {'city': 'San Francisco'})
        self.assertEqual(response.context['total_count'], 2)

    def test_filter_state(self):
        """Test filter by state"""
        response = self.client.get(reverse('screen1'), {'state': 'California'})
        self.assertEqual(response.context['total_count'], 3)

    def test_text_search(self):
        """Test text search"""
        response = self.client.get(reverse('screen1'), {'search_query': 'Beach'})
        self.assertEqual(response.context['total_count'], 1)

    def test_combined_filters(self):
        """Test combining filters"""
        response = self.client.get(reverse('screen1'), {
            'opportunity_type': 'volunteer',
            'location_type': 'remote'
        })
        self.assertEqual(response.context['total_count'], 1)
