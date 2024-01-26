from django.db import models
from django.contrib.auth.models import User
import manual.models as manual_models


class DailyCheck(models.Model):
    """
        Дневная смена,
        Может быть несколько для одной транзакции
    """

    class Status(models.TextChoices):
        CRITICAL = 'CR', 'Критично'
        WARNING = 'WA', 'Предупреждение'
        CONFIRM = 'CO', 'Без замечаний'

    photo = models.ManyToManyField(manual_models.Photo, verbose_name='Фото')

    city = models.ForeignKey(manual_models.City, on_delete=models.CASCADE, verbose_name='Город')
    car = models.ForeignKey(manual_models.Car, on_delete=models.CASCADE, verbose_name='Автомобиль')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')

    defect = models.TextField(verbose_name='Примечание')
    defect_status = models.CharField(max_length=2, choices=Status.choices, default=Status.CONFIRM,
                                     verbose_name='Статус примечания')

    mileage = models.PositiveIntegerField(verbose_name='Пробег')

    key = models.CharField(max_length=500, verbose_name='Держатель ключей')
    document = models.CharField(max_length=500, verbose_name='Держатель документов')

    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата открытия')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата закрытия')

    active = models.BooleanField(default=True, verbose_name='Статус')

    class Meta:
        verbose_name_plural = 'Отчеты по автомобилям'
        ordering = ['-created']
        indexes = [
            models.Index(fields=['active', 'author'])
        ]

    def __str__(self):
        return f'Смена от {self.created} {self.car}'


class CarMigration(models.Model):
    """
        Транзацкция во время которой осуществляется нахождение
        автомобиля у конкртетного владельца в какой-то конкретный период
    """

    car = models.ForeignKey(manual_models.Car, on_delete=models.CASCADE, verbose_name='Автомобиль')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Временный владелец')

    daily_check = models.ManyToManyField(DailyCheck, verbose_name='Смены')

    active = models.BooleanField(default=True, verbose_name='Статус')  # Открыта / закрыта
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')

    class Meta:
        verbose_name_plural = 'Транзакции автомобилей'
        ordering = ['-created']
        indexes = [
            models.Index(fields=['active', 'author'])
        ]

    def __str__(self):
        return f'Транзакция от {self.created} {self.car}'
