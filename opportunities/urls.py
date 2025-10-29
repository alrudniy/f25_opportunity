from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    OpportunityApplicationViewSet,
    OpportunityViewSet,
    OrganizationProfileViewSet,
    VolunteerProfileViewSet,
)

router = DefaultRouter()
router.register(r'organization-profiles', OrganizationProfileViewSet, basename='organizationprofile')
router.register(r'volunteer-profiles', VolunteerProfileViewSet, basename='volunteerprofile')
router.register(r'opportunities', OpportunityViewSet, basename='opportunity')
router.register(r'applications', OpportunityApplicationViewSet, basename='opportunityapplication')

urlpatterns = [
    path('', include(router.urls)),
]
