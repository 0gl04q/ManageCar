from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>', views.get_car, name='car'),
    path('', views.get_car_list, name='car_list')
]
