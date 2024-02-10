from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CarMigration, DailyCheck
from manual.models import CarParam


@receiver(post_save, sender=CarMigration)
def create_car_migration(sender, instance: CarMigration, created: bool, **kwargs):
    car_parameters = instance.car.parameters
    if created:
        car_parameters.status = CarParam.Status.RESERVE
        car_parameters.save()
    else:
        car_parameters.status = CarParam.Status.FREE
        car_parameters.save()


@receiver(post_save, sender=DailyCheck)
def create_daily_check(sender, instance: DailyCheck, created: bool, **kwargs):
    car_parameters = instance.car.parameters
    if created:
        car_parameters.status = CarParam.Status.JOB
        car_parameters.save()
    else:
        car_parameters.status = CarParam.Status.RESERVE
        car_parameters.save()
