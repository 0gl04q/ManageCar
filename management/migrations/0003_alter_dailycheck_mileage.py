# Generated by Django 5.0.1 on 2024-01-30 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_alter_dailycheck_city_alter_dailycheck_defect_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailycheck',
            name='mileage',
            field=models.PositiveIntegerField(default=0, verbose_name='Пробег'),
        ),
    ]
