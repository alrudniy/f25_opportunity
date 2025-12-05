from django.contrib import admin
from django.urls import path, include
from accounts.views import PostOnlyLogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('accounts/', include('accounts.urls')),
    path('logout/', PostOnlyLogoutView.as_view(), name='logout'),
]
