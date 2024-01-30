from django.urls import path
from django.shortcuts import redirect, reverse
from . import views


urlpatterns = [
    path('', views.redirect_view, name='main'),
    path('car_list/', views.get_all_car, name='car_list'),
    path('car_migration/<int:car_id>/', views.create_car_migration, name='car_migration'),
    path('car_return/<int:car_id>/', views.car_return, name='car_return'),
    path('create_daily_check/<int:car_id>/', views.create_daily_check, name='create_daily_check'),
    path('close_daily_check/<int:car_id>/', views.close_daily_check, name='close_daily_check'),
    path('profile/', views.get_profile, name='profile')
]
