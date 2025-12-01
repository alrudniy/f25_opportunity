from django.db import models

class Volunteer(models.Model):
    name = models.CharField(max_length=100)
    hours_contributed = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    volunteers_needed = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Opportunity(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    total_hours = models.IntegerField(default=0)

    def __str__(self):
        return self.name
