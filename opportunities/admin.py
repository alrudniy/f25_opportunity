# opportunities/admin.py
from django.contrib import admin
from .models import (
    OrganizationProfile,
    VolunteerProfile,
    Opportunity,
    OpportunityApplication,
    Subscription,
    Notification,
)

@admin.register(OrganizationProfile)
class OrganizationProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user")
    search_fields = ("name", "user__email", "user__username")

@admin.register(VolunteerProfile)
class VolunteerProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", )
    search_fields = ("user__email", "user__username", )

@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "organization")
    search_fields = ("title", "organization__name")

@admin.register(OpportunityApplication)
class OpportunityApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "opportunity", "volunteer", "applied_at")
    search_fields = ("opportunity__title", "volunteer__user__email")

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "organization", "created_at")
    search_fields = ("student__user__email", "organization__name")

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "recipient", "message", "is_read", "created_at")
    list_filter = ("is_read",)
    search_fields = ("recipient__email", "message")
