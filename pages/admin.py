from django.contrib import admin
from .models import Opportunity, Application, Experience, Achievement

@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization')
    list_filter = ('organization',)
    search_fields = ('title', 'description')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'opportunity', 'status', 'applied_date')
    list_filter = ('status', 'applied_date', 'opportunity__organization')
    search_fields = ('student__username', 'opportunity__title')
    raw_id_fields = ('student', 'opportunity')

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('student', 'title', 'opportunity', 'date_completed')
    list_filter = ('date_completed',)
    search_fields = ('student__username', 'title', 'description')
    raw_id_fields = ('student', 'opportunity')

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('student', 'title', 'date_completed')
    list_filter = ('date_completed',)
    search_fields = ('student__username', 'title')
    raw_id_fields = ('student',)
