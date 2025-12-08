from django.urls import path
from . import views
from accounts import views as accounts_views # Import accounts views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('screen1/', views.screen1, name='screen1'),
    path('screen2/', views.screen2, name='screen2'),
    path('screen3/', views.screen3, name='screen3'),
    path('about/', views.about, name='about'), # Added URL for About page
    path('company/about/', accounts_views.company_about, name='company_about'), # Point to accounts_views
]
