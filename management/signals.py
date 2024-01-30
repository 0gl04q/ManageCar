from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CarMigration
from manual.models import CarParam


@receiver(post_save, sender=CarMigration)
def create_car_migration(sender, instance: CarMigration, created: bool, **kwargs):
    if created:
        car_parameters = instance.car.parameters
        car_parameters.status = CarParam.Status.RESERVE
        car_parameters.save()
