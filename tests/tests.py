from django.test import TestCase                                                                                                   
from django.urls import reverse                                                                                                    
from django.contrib.auth import get_user_model                                                                                     
import datetime

from pages.models import Achievement                                                                                                                    
                                                                                                 
                                                                                                                                   
User = get_user_model()                                                                                                            
                                                                                                                                   
                                                                                                                                   
class AchievementPageTests(TestCase):                                                                                              
                                                                                                                                   
    def setUp(self):                                                                                                               
        self.student_user = User.objects.create_user(                                                                              
            username='studentuser',                                                                                                
            email='student@example.com',                                                                                           
            password='testpassword',                                                                                               
            user_type=User.UserType.STUDENT                                                                                        
        )                                                                                                                          
                                                                                                                                   
    def test_achievements_page_redirects_for_anonymous_user(self):                                                                 
        response = self.client.get(reverse('student_achievements'))                                                                
        self.assertEqual(response.status_code, 302)                                                                                
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('student_achievements')}")                               
                                                                                                                                   
    def test_achievements_page_accessible_for_student(self):                                                                       
        self.client.login(username='studentuser', password='testpassword')                                                         
        response = self.client.get(reverse('student_achievements'))                                                                
        self.assertEqual(response.status_code, 200)                                                                                
        self.assertTemplateUsed(response, 'pages/student_achievements.html')                                                       
                                                                                                                                   
    def test_student_can_add_achievement(self):                                                                                    
        self.client.login(username='studentuser', password='testpassword')                                                         
        url = reverse('student_achievements')                                                                                      
        achievement_data = {                                                                                                       
            'title': 'Graduated with Honors',                                                                                      
            'description': 'Achieved a 4.0 GPA.',                                                                                  
            'date_completed': '2025-05-20'                                                                                         
        }                                                                                                                          
        response = self.client.post(url, achievement_data, follow=True)                                                            
                                                                                                                                   
        self.assertEqual(response.status_code, 200)                                                                                
        self.assertTrue(Achievement.objects.filter(student=self.student_user, title='Graduated with Honors').exists())             
        self.assertContains(response, 'Graduated with Honors')                                                                     
        self.assertContains(response, 'Achieved a 4.0 GPA.')                                                                       
                                                                                                                                   
    def test_student_sees_only_their_achievements(self):                                                                           
        # Create another student and their achievement                                                                             
        other_student = User.objects.create_user(                                                                                  
            username='otherstudent',                                                                                               
            email='other@example.com',                                                                                             
            password='testpassword',                                                                                               
            user_type=User.UserType.STUDENT                                                                                        
        )                                                                                                                          
        Achievement.objects.create(                                                                                                
            student=other_student,                                                                                                 
            title='Other Student Achievement',                                                                                     
            description='This should not be visible.',                                                                             
            date_completed=datetime.date.today()                                                                                   
        )                                                                                                                          
                                                                                                                                   
        # Create achievement for the main student                                                                                  
        Achievement.objects.create(                                                                                                
            student=self.student_user,                                                                                             
            title='My Own Achievement',                                                                                            
            description='This should be visible.',                                                                                 
            date_completed=datetime.date.today()                                                                                   
        )                                                                                                                          
                                                                                                                                   
        self.client.login(username='studentuser', password='testpassword')                                                         
        response = self.client.get(reverse('student_achievements'))                                                                
                                                                                                                                   
        self.assertContains(response, 'My Own Achievement')                                                                        
        self.assertNotContains(response, 'Other Student Achievement')

