from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    NotificationListView,
    NotificationReadView,
    OpportunityApplicationViewSet,
    OpportunityViewSet,
    OrganizationProfileViewSet,
    SubscribeView,
    UnsubscribeView,
    VolunteerProfileViewSet,
)

router = DefaultRouter()
router.register(r'organization-profiles', OrganizationProfileViewSet, basename='organizationprofile')
router.register(r'volunteer-profiles', VolunteerProfileViewSet, basename='volunteerprofile')
router.register(r'opportunities', OpportunityViewSet, basename='opportunity')
router.register(r'applications', OpportunityApplicationViewSet, basename='opportunityapplication')

urlpatterns = [
    path('', include(router.urls)),
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
    path('unsubscribe/', UnsubscribeView.as_view(), name='unsubscribe'),
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/read/', NotificationReadView.as_view(), name='notification-read'),
]
