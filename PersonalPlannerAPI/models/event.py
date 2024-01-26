from django.db import models

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("PPUser", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    start_datetime = models.DateTimeField()
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    zipcode = models.IntegerField()