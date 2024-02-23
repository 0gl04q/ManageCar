from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Owner(models.Model):
    """
        Владельцы автомобилей
    """
    name = models.CharField(max_length=150, verbose_name='ФИО')

    class Meta:
        verbose_name_plural = 'Владельцы'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/manual/owner/{self.pk}'


class CarMark(models.Model):
    """
        Марки автомобилей
    """
    name = models.CharField(max_length=50, verbose_name='Наименование')

    class Meta:
        verbose_name_plural = 'Марки'

    def __str__(self):
        return self.name


class CarModel(models.Model):
    """
        Модели автомобилей
    """
    name = models.CharField(max_length=50, verbose_name='Наименование')
    mark = models.ForeignKey(CarMark, on_delete=models.CASCADE, verbose_name='Марка')

    class Meta:
        verbose_name_plural = 'Модели'

    def __str__(self):
        return f'{self.mark} {self.name}'


class CarManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True, parameters__status=CarParam.Status.FREE)


class Car(models.Model):
    """
        Модель Автомобиля
        для каждого автомобился создаются CarParam для описания дополнительных параметров
    """

    objects = models.Manager()
    free_cars = CarManager()

    name = models.CharField(max_length=10, verbose_name='Имя', null=True)
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, verbose_name='Марка/Модель')
    gos_number = models.CharField(max_length=9, verbose_name='Гос. номер')
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, verbose_name='Владелец')
    mileage = models.PositiveIntegerField(verbose_name='Пробег')
    slug = models.SlugField(max_length=9, verbose_name='SLUG-ссылка')
    year = models.PositiveIntegerField(
        verbose_name='Год выпуска',
        default=2000,
        validators=(MinValueValidator(1950), MaxValueValidator(now().year))
    )

    active = models.BooleanField(default=True, verbose_name='Статус')

    class Meta:
        verbose_name_plural = 'Автомобили'

    def __str__(self):
        return f'{self.name}'

    def get_active_daily_check(self):
        return self.dailycheck_set.get(active=True)

    def get_last_daily_check(self):
        return self.dailycheck_set.order_by('-created').first()

    def get_last_close_daily_check(self):
        return self.dailycheck_set.order_by('active', '-created').first()

    def get_now_daily_check(self):
        return self.dailycheck_set.filter(created__day=now().day)

    def get_now_author(self):
        transaction = self.carmigration_set.filter(active=True).first()
        return transaction.author if transaction else None

    def get_ts(self):
        return self.parameters.technical_service - self.mileage

    def get_grm(self):
        return self.parameters.grm - self.mileage

    def get_insurance(self):
        return self.parameters.insurance.strftime('%d.%m.%Y')

    def get_absolute_url(self):
        return reverse(viewname='management:info_car', args=(self.pk,))


class CarParam(models.Model):
    """
        Дополнительные параметры автомобиля
    """

    class Status(models.TextChoices):
        JOB = '1', 'В работе'
        RESERVE = '2', 'Занят'
        TECH_SERVICE = '3', 'На ТО'
        FREE = '4', 'Свободен'

    class Meta:
        verbose_name_plural = 'Автомобиль. Дополнительные сведения'

    car = models.OneToOneField(Car, on_delete=models.CASCADE, verbose_name='Автомобиль', related_name='parameters')
    insurance = models.DateField(verbose_name='Страховка')
    technical_service = models.PositiveIntegerField(verbose_name='ТО')
    grm = models.PositiveIntegerField(verbose_name='ГРМ')

    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.FREE,
        verbose_name='Статус'
    )

    def __str__(self):
        return f'{self.car} - {self.get_status_display()}'


class City(models.Model):
    """
        Города
    """
    name = models.CharField(max_length=100, verbose_name='Наименование')

    class Meta:
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name


class Photo(models.Model):
    """
        Фото автомобиля
        ManyToMany для одной транзакции
        По логике ежедневны в рамках одной транзакции
    """
    created = models.DateTimeField(auto_now=True, verbose_name='Дата создания')
    name = models.CharField(max_length=150, verbose_name='Имя фотографии', null=True)
    file = models.ImageField(upload_to='car_images', verbose_name='Фото', null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')

    class Meta:
        verbose_name_plural = 'Фотографии'

    def __str__(self):
        return f'{self.file.name}'
