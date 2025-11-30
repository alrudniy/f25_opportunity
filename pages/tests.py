from django.test import TestCase

from django.test import TestCase                                                                                                             
                                                                                                                                             
# Create your tests here.                                                                                                                    
=======                                                                                                                                      
from django.test import TestCase                                                                                                             
from django.urls import reverse                                                                                                              
                                                                                                                                             
from .models import User                                                                                                                     
                                                                                                                                             
                                                                                                                                             
class RegistrationAndLoginViewTestCase(TestCase):                                                                                            
    def _test_user_type_flow(self, user_type, email):                                                                                        
        # Test that a user-type specific login page is displayed. This                                                                       
        # simulates a user clicking a user-type button on the welcome page.                                                                  
        login_url = reverse('login') + f'?user_type={user_type}'                                                                             
        response = self.client.get(login_url)                                                                                                
        self.assertEqual(response.status_code, 200)                                                                                          
        self.assertContains(response, f'Sign in as {user_type.capitalize()}')                                                                
                                                                                                                                             
        # Test the registration form for the given user type. This simulates                                                                 
        # the user navigating from the login page to the registration page.                                                                  
        register_url = reverse('register') + f'?user_type={user_type}'                                                                       
        response = self.client.get(register_url)                                                                                             
        self.assertEqual(response.status_code, 200)                                                                                          
        self.assertEqual(response.context['form'].initial.get('user_type'), user_type)                                                       
                                                                                                                                             
        # Register a new user                                                                                                                
        self.assertEqual(User.objects.count(), 0)                                                                                            
        form_data = {                                                                                                                        
            'username': email,                                                                                                               
            'password1': 'testpass123',                                                                                                      
            'password2': 'testpass123',                                                                                                      
            'user_type': user_type,                                                                                                          
        }                                                                                                                                    
                                                                                                                                             
        response = self.client.post(reverse('register'), data=form_data)                                                                     
                                                                                                                                             
        self.assertRedirects(response, reverse('screen1'))                                                                                   
                                                                                                                                             
        # Verify user creation                                                                                                               
        self.assertEqual(User.objects.count(), 1)                                                                                            
        user = User.objects.first()                                                                                                          
        self.assertEqual(user.username, email)                                                                                               
        self.assertEqual(user.user_type, user_type)                                                                                          
                                                                                                                                             
        # Verify user is logged in                                                                                                           
        self.assertIn('_auth_user_id', self.client.session)                                                                                  
                                                                                                                                             
    def test_student_flow(self):                                                                                                             
        """                                                                                                                                  
        Tests that an anonymous user can go through the student registration                                                                 
        flow and create a student user.                                                                                                      
        """                                                                                                                                  
        self._test_user_type_flow('student', 'student@example.com')                                                                          
                                                                                                                                             
    def test_organization_flow(self):                                                                                                        
        """                                                                                                                                  
        Tests that an anonymous user can go through the organization                                                                         
        registration flow and create an organization user.                                                                                   
        """                                                                                                                                  
        self._test_user_type_flow('organization', 'org@example.com')
