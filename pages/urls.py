from django.urls import path
from . import views
from . import buggy_view            # the intentionally buggy version (lives in pages/)
from . import buggy_view_fixed      # the fixed version (also in pages/)

urlpatterns = [
    path('', views.welcome, name='welcome'),

    path('screen1/', views.screen1, name='screen1'),
    path('screen2/', views.screen2, name='screen2'),
    path('screen3/', views.screen3, name='screen3'),

    path('achievements/', views.student_achievements, name='student_achievements'),
    path('faq/', views.faq, name='faq'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('notifications/', views.notifications, name='notifications'),
    path('company/home/', views.company_home, name='company_home'),

    # Debug assignment routes
    path('buggy/', buggy_view.buggy_search, name='buggy_search'),
    path('buggy_fixed/', buggy_view_fixed.buggy_search, name='buggy_search_fixed'),
]
