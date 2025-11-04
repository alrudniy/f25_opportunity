from rest_framework import generics, permissions, serializers, status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User

from .models import (
    Notification,
    Opportunity,
    OpportunityApplication,
    OrganizationProfile,
    Subscription,
    VolunteerProfile,
)
from .permissions import IsOrganizationUser, IsOwnerOrReadOnly, IsStudentUser
from .serializers import (
    NotificationSerializer,
    OpportunityApplicationSerializer,
    OpportunitySerializer,
    OrganizationProfileSerializer,
    SubscriptionSerializer,
    VolunteerProfileSerializer,
)


def send_opportunity_notifications(opportunity):
    """
    Creates notifications for students subscribed to the organization that posted the opportunity.
    """
    organization = opportunity.organization
    subscriptions = Subscription.objects.filter(organization=organization)
    for sub in subscriptions:
        student_user = sub.student.user
        message = f"New opportunity from {organization.name}: {opportunity.title}"
        Notification.objects.create(recipient=student_user, message=message)


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
        opportunity = serializer.save(organization=self.request.user.organization_profile)
        send_opportunity_notifications(opportunity)


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


class SubscribeView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudentUser]

    def perform_create(self, serializer):
        organization_id = self.request.data.get('organization_id')
        if not organization_id:
            raise serializers.ValidationError({"organization_id": "This field is required."})

        try:
            organization = OrganizationProfile.objects.get(id=organization_id)
        except OrganizationProfile.DoesNotExist:
            raise serializers.ValidationError({"organization_id": "Organization does not exist."})

        if not hasattr(self.request.user, 'volunteer_profile'):
            raise PermissionDenied("You must have a volunteer profile to subscribe.")

        volunteer_profile = self.request.user.volunteer_profile

        if Subscription.objects.filter(student=volunteer_profile, organization=organization).exists():
            raise serializers.ValidationError({"detail": "You are already subscribed to this organization."})

        serializer.save(student=volunteer_profile, organization=organization)


class UnsubscribeView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsStudentUser]

    def delete(self, request, *args, **kwargs):
        organization_id = request.data.get('organization_id')
        if not organization_id:
            return Response({"detail": "organization_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        if not hasattr(request.user, 'volunteer_profile'):
            return Response({"detail": "You must have a volunteer profile to unsubscribe."}, status=status.HTTP_403_FORBIDDEN)

        try:
            organization = OrganizationProfile.objects.get(id=organization_id)
            subscription = Subscription.objects.get(
                student=request.user.volunteer_profile,
                organization=organization
            )
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except OrganizationProfile.DoesNotExist:
            return Response({"detail": "Organization not found."}, status=status.HTTP_404_NOT_FOUND)
        except Subscription.DoesNotExist:
            return Response({"detail": "Subscription not found."}, status=status.HTTP_404_NOT_FOUND)


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by('-created_at')


class NotificationReadView(generics.UpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['patch']

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

    def perform_update(self, serializer):
        serializer.save(is_read=True)
