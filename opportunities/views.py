from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied

from accounts.models import User

from .models import (
    Opportunity,
    OpportunityApplication,
    OrganizationProfile,
    VolunteerProfile,
)
from .permissions import IsOrganizationUser, IsOwnerOrReadOnly, IsStudentUser
from .serializers import (
    OpportunityApplicationSerializer,
    OpportunitySerializer,
    OrganizationProfileSerializer,
    VolunteerProfileSerializer,
)


class OrganizationProfileViewSet(viewsets.ModelViewSet):
    queryset = OrganizationProfile.objects.all()
    serializer_class = OrganizationProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        if self.request.user.user_type == User.UserType.ORGANIZATION:
            serializer.save(user=self.request.user)
        else:
            raise PermissionDenied("Only organization users can create organization profiles.")


class VolunteerProfileViewSet(viewsets.ModelViewSet):
    queryset = VolunteerProfile.objects.all()
    serializer_class = VolunteerProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        if self.request.user.user_type == User.UserType.STUDENT:
            serializer.save(user=self.request.user)
        else:
            raise PermissionDenied("Only student users can create volunteer profiles.")


class OpportunityViewSet(viewsets.ModelViewSet):
    queryset = Opportunity.objects.all()
    serializer_class = OpportunitySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, IsOrganizationUser]
        else:  # update, partial_update, destroy
            permission_classes = [permissions.IsAuthenticated, IsOrganizationUser, IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        if not hasattr(self.request.user, 'organization_profile'):
            raise PermissionDenied('You must have an organization profile to create opportunities.')
        serializer.save(organization=self.request.user.organization_profile)


class OpportunityApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = OpportunityApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return OpportunityApplication.objects.none()

        if user.user_type == User.UserType.STUDENT and hasattr(user, 'volunteer_profile'):
            return OpportunityApplication.objects.filter(volunteer=user.volunteer_profile)
        elif user.user_type == User.UserType.ORGANIZATION and hasattr(user, 'organization_profile'):
            return OpportunityApplication.objects.filter(opportunity__organization=user.organization_profile)

        return OpportunityApplication.objects.none()

    def perform_create(self, serializer):
        if not hasattr(self.request.user, 'volunteer_profile'):
            raise PermissionDenied('You must have a volunteer profile to apply.')
        serializer.save(volunteer=self.request.user.volunteer_profile)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [permissions.IsAuthenticated, IsStudentUser]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()
