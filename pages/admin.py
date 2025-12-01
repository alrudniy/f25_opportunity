from django.contrib import admin
from .models import Volunteer, Event, Opportunity

# Register your models here.
admin.site.register(Volunteer)
admin.site.register(Event)
admin.site.register(Opportunity)
