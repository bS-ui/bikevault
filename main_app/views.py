from django.shortcuts import render, redirect
from .models import Bike, Photo
import uuid
import boto3
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'brandon-s-bike-vault'

class Home(LoginView):
  template_name = 'home.html'

@login_required
def bike_index(request):
  bikes = Bike.objects.filter(user=request.user)
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

class BikeCreate(LoginRequiredMixin, CreateView):
  model = Bike
  fields = ['model', 'make', 'year', 'description']
  success_url = '/bikes/'

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

@login_required
def bike_detail(request, bike_id):
  bike = Bike.objects.get(id=bike_id)
  return render(request, 'bikes/detail.html', { 'bike': bike })

class BikeUpdate(LoginRequiredMixin, UpdateView):
  model = Bike
  fields = ['model', 'make', 'year', 'description']

class BikeDelete(LoginRequiredMixin, DeleteView):
  model = Bike
  success_url = '/bikes/'

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('bike-index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)