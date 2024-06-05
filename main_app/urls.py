from django.urls import path
from . import views

urlpatterns = [
  path('bikes/', views.bike_index, name='bike-index'),
  path('bikes/<int:bike_id>/add-photo/', views.add_photo, name='add-photo'),
  path('bikes/create/', views.BikeCreate.as_view(), name='bike-create'),
  path('bikes/<int:bike_id>/', views.bike_detail, name='bike-detail'),
  path('bikes/<int:pk>/update/', views.BikeUpdate.as_view(), name='bike-update'),
  path('bikes/<int:pk>/delete/', views.BikeDelete.as_view(), name='bike-delete'),
  path('', views.Home.as_view(), name='home'),
  path('accounts/signup/', views.signup, name='signup'),
]