from django.shortcuts import render, redirect
from .models import Bike, Photo
import uuid
import boto3

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'brandon-s-bike-vault'

def home(request):
  return render(request, 'home.html')

def bike_index(request):
  bikes = Bike.objects.all()
  return render(request, 'bikes/index.html', { 'bikes': bikes })

def add_photo(request, bike_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex + photo_file.name[photo_file.name.rfind('.'):]
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      photo = Photo(url=url, bike_id=bike_id)
      bike_photo = Photo.objects.filter(bike_id=bike_id)
      if bike_photo.first():
        bike_photo.first().delete()
      photo.save()
    except Exception as err:
      print('An error occurred uploading file to S3: %s' % err)
  return redirect('bike-index', bike_id=bike_id)