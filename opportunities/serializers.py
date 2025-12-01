from rest_framework import serializers

from .models import (
    Notification,
    Opportunity,
    OpportunityApplication,
    OrganizationProfile,
    Subscription,
    VolunteerProfile,
)


class OrganizationProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationProfile
        fields = ['id', 'user', 'name', 'description']
        read_only_fields = ['user']


class VolunteerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerProfile
        fields = ['id', 'user', 'skills', 'interests']
        read_only_fields = ['user']


class OpportunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Opportunity
        fields = ['id', 'organization', 'title', 'description', 'created_at', 'updated_at']
        read_only_fields = ['organization']


class OpportunityApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpportunityApplication
        fields = ['id', 'opportunity', 'volunteer', 'applied_at']
        read_only_fields = ['volunteer']


class SubscriptionSerializer(serializers.ModelSerializer):
    organization_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Subscription
        fields = ['id', 'student', 'organization', 'created_at', 'organization_id']
        read_only_fields = ['id', 'student', 'organization', 'created_at']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'message', 'created_at', 'is_read']
        read_only_fields = ['id', 'recipient', 'message', 'created_at']
