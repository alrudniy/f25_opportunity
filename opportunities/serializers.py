from rest_framework import serializers

from .models import (
    Opportunity,
    OpportunityApplication,
    OrganizationProfile,
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
