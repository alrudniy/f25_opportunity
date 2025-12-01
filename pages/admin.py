from django.contrib import admin

from .models import Application, Opportunity

# Register your models here.
admin.site.register(Opportunity)
admin.site.register(Application)
