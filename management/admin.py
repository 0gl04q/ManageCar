from django.contrib import admin
from . import models


@admin.register(models.CarMigration)
class CarMigrationAdmin(admin.ModelAdmin):
    list_display = ['car', 'author', 'created', 'updated', 'active']
    list_filter = ['author', 'car', 'active']
    date_hierarchy = 'created'
    ordering = ['-created', '-updated']


@admin.register(models.DailyCheck)
class DailyCheckAdmin(admin.ModelAdmin):
    list_display = ['car', 'author', 'city', 'created', 'updated', 'active']
    list_filter = ['author', 'car', 'city', 'active']
    date_hierarchy = 'created'
    ordering = ['-created', '-updated']