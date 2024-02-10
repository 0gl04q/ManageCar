from django.contrib import admin
from . import models


@admin.register(models.Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['file', 'created', 'author']
    list_filter = ['author']
    ordering = ['-created']
    date_hierarchy = 'created'


@admin.register(models.CarMark)
class CarMarkAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(models.CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['mark', 'name']
    list_filter = ['mark']
    search_fields = ['mark', 'name']


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
    raw_id_fields = ['car_model']


@admin.register(models.CarParam)
class CarParamAdmin(admin.ModelAdmin):
    list_display = ['car', 'insurance', 'technical_service', 'grm', 'status']
    list_filter = ['car', 'status']
    ordering = ['technical_service', 'grm']
