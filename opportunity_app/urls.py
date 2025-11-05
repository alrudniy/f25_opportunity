from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),

    # your app routes
    path('', include('pages.urls')),
    path('accounts/', include('accounts.urls')),

    # logout for your web app (redirects to welcome page)
    path('logout/', LogoutView.as_view(next_page='welcome'), name='logout'),

    # API routes
    path('api/', include('opportunities.urls')),

    # 👇 add this line for Django REST Framework browsable API login/logout
    path('api-auth/', include('rest_framework.urls')),

    path('api-auth/logout/', LogoutView.as_view(next_page='/api/'), name='drf_logout'),
]
