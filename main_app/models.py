from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Bike(models.Model):
  make = models.CharField(max_length=100)
  model = models.CharField(max_length=100)
  year = models.IntegerField()
  description = models.TextField(max_length=250)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.model
  
  def get_absolute_url(self):
    return reverse('bike-detail', kwargs={'bike_id': self.id})

class Photo(models.Model):
  url = models.CharField(max_length=250)
  # bike = models.OneToOneField(Bike, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for bike_id: {self.bike_id} @{self.url}"