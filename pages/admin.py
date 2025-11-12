from django.contrib import admin
from .models import Achievement
# Register your models here.
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'date_completed')
    search_fields = ['title', 'description']

admin.site.register(Achievement, AchievementAdmin)
