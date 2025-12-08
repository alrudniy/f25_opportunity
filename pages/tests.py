from django.test import TestCase                                                                                                                                                                                                                                                       
from django.contrib.auth import get_user_model                                                                                               
from django.test import TestCase                                                                                                             
from django.urls import reverse                                                                                                              
                                                                                                                                             
                                                                                                                                             
class CompanyAboutPageTest(TestCase):                                                                                                        
    """Tests for the company about page."""                                                                                                  
                                                                                                                                             
    def setUp(self):                                                                                                                         
        User = get_user_model()                                                                                                              
        self.user = User.objects.create_user(                                                                                                
            username="testorg",                                                                                                              
            email="testorg@example.com",                                                                                                     
            password="password123",                                                                                                          
            user_type=User.UserType.ORGANIZATION,                                                                                            
            first_name="Test",                                                                                                               
            last_name="Company",                                                                                                             
        )                                                                                                                                    
                                                                                                                                             
    def test_company_about_page_as_logged_in_user(self):                                                                                     
        """                                                                                                                                  
        Tests that a logged-in organization user can access the company about page                                                           
        and that the page displays correct information.                                                                                      
        """                                                                                                                                  
        self.client.login(username="testorg", password="password123")                                                                        
        response = self.client.get(reverse("company_about"))                                                                                 
                                                                                                                                             
        self.assertEqual(response.status_code, 200)                                                                                          
        self.assertTemplateUsed(response, "pages/company_about.html")                                                                        
        self.assertContains(response, f"About {self.user.display_name}")                                                                     
        self.assertContains(response, self.user.email)                                                                                       
        self.assertContains(response, "Mission")                                                                                             
        self.assertContains(response, "What Problems We Solve")
