from django.urls import path
from django.shortcuts import redirect, reverse
from . import views


urlpatterns = [
    path('', views.redirect_view, name='main'),
    path('car_list/', views.get_all_car, name='car_list'),

    path('car_migration/<int:car_id>/', views.create_car_migration, name='car_migration'),
    path('car_return/<int:car_id>/', views.car_return, name='car_return'),

    path('create_daily_check/<int:car_id>/', views.create_daily_check, name='create_daily_check'),
    path('close_daily_check/<int:daily_check_id>/', views.close_daily_check, name='close_daily_check'),
    path('close_daily_check/<int:daily_check_id>/<int:photo_num>/<str:title_action>', views.capture_photo, name='create_photo'),

    path('user_cars/', views.get_profile, name='user_cars'),

    path('manage_cars/', views.CarListView.as_view(), name='manage_cars'),
    path('info_car/<int:pk>', views.CarDetailView.as_view(), name='info_car'),
    path('edit_car/<int:pk>', views.edit_car, name='edit_car'),
    path('create_car/', views.create_car, name='create_car'),

    path('update_ts/<int:pk>', views.update_ts, name='update_ts'),
    path('update_grm/<int:pk>', views.update_grm, name='update_grm')
]
