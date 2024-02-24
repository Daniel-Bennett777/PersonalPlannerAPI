from django.db import models
from .category import Category
from django.utils import timezone

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("PPUser", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="events" )
    title = models.CharField(max_length=255)
    attendees = models.ManyToManyField("PPUser", related_name="events_attending", blank=True)
    description = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    event_date = models.DateField()
    event_time = models.TimeField(default=timezone.now)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    zipcode = models.IntegerField()