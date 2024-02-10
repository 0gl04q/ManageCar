from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from . import models


@admin.register(models.CarMigration)
class CarMigrationAdmin(admin.ModelAdmin):
    list_display = ['car', 'author', 'created', 'updated', 'active']
    list_filter = ['author', 'car', 'active']
    date_hierarchy = 'created'
    ordering = ['-created', '-updated']


@admin.register(models.DailyCheck)
class DailyCheckAdmin(SummernoteModelAdmin):
    summernote_fields = ('defect', )
    list_display = ['car', 'author', 'city', 'created', 'updated', 'active']
    list_filter = ['author', 'car', 'city', 'active']
    date_hierarchy = 'created'
    ordering = ['-created', '-updated']