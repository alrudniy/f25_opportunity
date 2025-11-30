from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
# Import views from accounts and pages apps if needed for root URLs
# from accounts.views import RegisterView, CustomLoginView # Example if you want to use them directly here

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include URLs from the pages app
    path('', include('pages.urls')),
    # Include URLs from the accounts app
    path('accounts/', include('accounts.urls')),
    # Logout URL - can be defined here or in accounts.urls
    # If defined in accounts.urls, this line might be redundant or need adjustment.
    # For clarity, let's keep it here if it's a top-level logout.
    # If LogoutView is handled in accounts.urls, this can be removed.
    # path('logout/', LogoutView.as_view(next_page='welcome'), name='logout'), # This is now handled in accounts.urls
]
