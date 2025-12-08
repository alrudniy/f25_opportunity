from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from pages.models import Achievement
from pages.forms import AchievementForm
from datetime import date

User = get_user_model()

class PagesViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Create different user types
        self.student_user = User.objects.create_user(
            username='student@example.com', email='student@example.com', password='password123', user_type=User.UserType.STUDENT
        )
        self.organization_user = User.objects.create_user(
            username='org@example.com', email='org@example.com', password='password123', user_type=User.UserType.ORGANIZATION
        )
        self.admin_user = User.objects.create_superuser( # Use create_superuser for admin
            username='admin@example.com', email='admin@example.com', password='password123'
        )
        # Assign user_type to admin_user, as the User model extends AbstractUser and adds it
        self.admin_user.user_type = User.UserType.ORGANIZATION
        self.admin_user.save()

        self.login_url = reverse('login')
        self.welcome_url = reverse('welcome')
        self.screen1_url = reverse('screen1')
        self.screen2_url = reverse('screen2')
        self.screen3_url = reverse('screen3')
        self.achievements_url = reverse('student_achievements')
        self.faq_url = reverse('faq')
        self.dashboard_url = reverse('dashboard')

    # Test unauthenticated access to protected views
    def test_unauthenticated_access_redirects_to_login(self):
        protected_urls = [
            self.screen1_url, self.screen2_url, self.screen3_url, self.achievements_url
        ]
        for url in protected_urls:
            response = self.client.get(url)
            self.assertRedirects(response, f'{self.login_url}?next={url}')

    # Test public views
    def test_welcome_view(self):
        response = self.client.get(self.welcome_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/welcome.html')

    def test_faq_view(self):
        response = self.client.get(self.faq_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/faq.html')

    def test_dashboard_view(self):
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/dashboard.html')

    # Test screen views for different user types
    def test_screen_views_student_user(self):
        self.client.login(username=self.student_user.username, password='password123')
        for url in [self.screen1_url, self.screen2_url, self.screen3_url]:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, f'pages/{url.split("/")[-2]}.html')
            self.assertIn('role', response.context)
            self.assertEqual(response.context['role'], 'Student')

    def test_screen_views_organization_user(self):
        self.client.login(username=self.organization_user.username, password='password123')
        for url in [self.screen1_url, self.screen2_url, self.screen3_url]:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, f'pages/{url.split("/")[-2]}.html')
            self.assertIn('role', response.context)
            self.assertEqual(response.context['role'], 'Organization')

    def test_screen_views_admin_user(self):
        # Admin user's user_type is 'organization' as per setUp
        self.client.login(username=self.admin_user.username, password='password123')
        for url in [self.screen1_url, self.screen2_url, self.screen3_url]:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, f'pages/{url.split("/")[-2]}.html')
            self.assertIn('role', response.context)
            self.assertEqual(response.context['role'], 'Organization') # Based on admin_user.user_type set in setUp


    # Test student_achievements view
    def test_student_achievements_unauthenticated(self):
        response = self.client.get(self.achievements_url)
        self.assertRedirects(response, f'{self.login_url}?next={self.achievements_url}')

    def test_student_achievements_non_student_redirects(self):
        # Test with an organization user
        self.client.login(username=self.organization_user.username, password='password123')
        response = self.client.get(self.achievements_url)
        self.assertRedirects(response, self.screen1_url)

        # Test with an admin user
        self.client.login(username=self.admin_user.username, password='password123')
        response = self.client.get(self.achievements_url)
        self.assertRedirects(response, self.screen1_url)

    def test_student_achievements_get_no_achievements(self):
        self.client.login(username=self.student_user.username, password='password123')
        response = self.client.get(self.achievements_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/student_achievements.html')
        self.assertIn('achievements', response.context)
        self.assertEqual(len(response.context['achievements']), 0)
        self.assertIsInstance(response.context['form'], AchievementForm)

    def test_student_achievements_get_with_achievements(self):
        self.client.login(username=self.student_user.username, password='password123')
        Achievement.objects.create(
            student=self.student_user, title='First Achievement', description='Description 1', date_completed=date(2023, 1, 1)
        )
        Achievement.objects.create(
            student=self.student_user, title='Second Achievement', description='Description 2', date_completed=date(2023, 2, 1)
        )
        response = self.client.get(self.achievements_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/student_achievements.html')
        self.assertIn('achievements', response.context)
        self.assertEqual(len(response.context['achievements']), 2)
        # Check order by '-date_completed'
        self.assertEqual(response.context['achievements'][0].title, 'Second Achievement')
        self.assertEqual(response.context['achievements'][1].title, 'First Achievement')

    def test_student_achievements_post_valid_data(self):
        self.client.login(username=self.student_user.username, password='password123')
        initial_achievement_count = Achievement.objects.count()
        post_data = {
            'title': 'New Achievement',
            'description': 'A description of the new achievement.',
            'date_completed': '2023-03-15'
        }
        response = self.client.post(self.achievements_url, post_data)
        self.assertRedirects(response, self.achievements_url)
        self.assertEqual(Achievement.objects.count(), initial_achievement_count + 1)
        new_achievement = Achievement.objects.get(title='New Achievement')
        self.assertEqual(new_achievement.student, self.student_user)
        self.assertEqual(new_achievement.description, 'A description of the new achievement.')
        self.assertEqual(new_achievement.date_completed, date(2023, 3, 15))

    def test_student_achievements_post_invalid_data(self):
        self.client.login(username=self.student_user.username, password='password123')
        initial_achievement_count = Achievement.objects.count()
        # Missing required title
        post_data = {
            'description': 'A description.',
            'date_completed': '2023-03-15'
        }
        response = self.client.post(self.achievements_url, post_data)
        self.assertEqual(response.status_code, 200) # Should re-render with errors
        self.assertTemplateUsed(response, 'pages/student_achievements.html')
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)
        self.assertIn('title', response.context['form'].errors)
        self.assertEqual(Achievement.objects.count(), initial_achievement_count) # No achievement created

    def test_student_achievements_post_extreme_data_long_fields(self):
        self.client.login(username=self.student_user.username, password='password123')
        initial_achievement_count = Achievement.objects.count()

        # Assuming CharField max_length is 255 for 'title' and TextField for 'description'
        long_title = "A" * 255
        long_description = "B" * 1000

        post_data = {
            'title': long_title,
            'description': long_description,
            'date_completed': '2024-12-31'
        }
        response = self.client.post(self.achievements_url, post_data)
        self.assertRedirects(response, self.achievements_url)
        self.assertEqual(Achievement.objects.count(), initial_achievement_count + 1)
        new_achievement = Achievement.objects.get(title=long_title)
        self.assertEqual(new_achievement.description, long_description)
        self.assertEqual(new_achievement.date_completed, date(2024, 12, 31))

    def test_student_achievements_post_extreme_data_current_date(self):
        self.client.login(username=self.student_user.username, password='password123')
        initial_achievement_count = Achievement.objects.count()

        today = date.today()
        post_data_today = {
            'title': 'Achievement Today',
            'description': 'Completed today.',
            'date_completed': today.strftime('%Y-%m-%d')
        }
        response_today = self.client.post(self.achievements_url, post_data_today)
        self.assertRedirects(response_today, self.achievements_url)
        self.assertEqual(Achievement.objects.count(), initial_achievement_count + 1)
        new_achievement_today = Achievement.objects.get(title='Achievement Today')
        self.assertEqual(new_achievement_today.date_completed, today)

    def test_student_achievements_post_invalid_date_format(self):
        self.client.login(username=self.student_user.username, password='password123')
        initial_achievement_count = Achievement.objects.count()
        post_data = {
            'title': 'Bad Date',
            'description': 'Invalid date format.',
            'date_completed': '2023/03/15' # Incorrect format
        }
        response = self.client.post(self.achievements_url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/student_achievements.html')
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)
        self.assertIn('date_completed', response.context['form'].errors)
        self.assertEqual(Achievement.objects.count(), initial_achievement_count)
