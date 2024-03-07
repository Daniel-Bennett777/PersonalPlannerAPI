from django.db import models
from django.contrib.auth.models import User

class PPUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="pp_user")
    # firstname = models.CharField(max_length=255)
    # lastname = models.CharField(max_length=255)
    # username = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    zipcode = models.IntegerField()
