from django.db import models

class Bike(models.Model):
  make = models.CharField(max_length=100)
  model = models.CharField(max_length=100)
  year = models.IntegerField()
  description = models.TextField(max_length=250)

  def __str__(self):
    return self.model

class Photo(models.Model):
  url = models.CharField(max_length=250)
  bike = models.OneToOneField(Bike, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for bike_id: {self.bike_id} @{self.url}"