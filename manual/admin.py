from django.contrib import admin
from . import models


@admin.register(models.Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(models.Photo)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ['photo', 'created', 'car', 'author', 'city']
    list_filter = ['car', 'author', 'city']
    ordering = ['-created']
    date_hierarchy = 'created'


@admin.register(models.CarMark)
class CarMarkAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(models.CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['mark', 'name']


@admin.register(models.City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(models.Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['gos_number', 'car_model', 'mileage', 'active']
    list_filter = ['car_model', 'active']
    prepopulated_fields = {
        'slug': ('gos_number',)
    }


@admin.register(models.CarParam)
class CarParamAdmin(admin.ModelAdmin):
    list_display = ['car', 'insurance', 'technical_service', 'grm', 'status']
    list_filter = ['car', 'status']
    ordering = ['technical_service', 'grm']
