# Generated by Django 5.0.1 on 2024-01-30 14:03

import django.db.models.deletion
import django.db.models.manager
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manual', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='car',
            managers=[
                ('free_cars', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='carparam',
            name='car',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='parameters', to='manual.car', verbose_name='Автомобиль'),
        ),
    ]
