from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('bikes', views.bike_index, name='bike-index'),
  path('bikes/<int:bike_id>/add-photo/', views.add_photo, name='add-photo'),
]