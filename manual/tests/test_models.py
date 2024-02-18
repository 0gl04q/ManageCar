from django.test import TestCase
from manual import models
from management import models as manager_models
from django.contrib.auth.models import User
from django.utils.timezone import now


class OwnerModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        models.Owner.objects.create(name='ТМА')

    def test_name_label(self):
        owner = models.Owner.objects.get(id=1)
        field_label = owner._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'ФИО')

    def test_name_max_length(self):
        owner = models.Owner.objects.get(id=1)
        max_length = owner._meta.get_field('name').max_length
        self.assertEqual(max_length, 150)

    def test_verbose_name_plural(self):
        owner = models.Owner.objects.get(id=1)
        verbose_name_plural = owner._meta.verbose_name_plural
        self.assertEquals(verbose_name_plural, 'Владельцы')

    def test_object_name_is_name(self):
        owner = models.Owner.objects.get(id=1)
        expected_object_name = owner.name
        self.assertEquals(expected_object_name, str(owner))

    def test_get_absolute_url(self):
        owner = models.Owner.objects.get(id=1)
        self.assertEquals(owner.get_absolute_url(), '/manual/owner/1')


class CarMarkModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        models.CarMark.objects.create(name='LADA')

    def test_name_label(self):
        mark = models.CarMark.objects.get(id=1)
        field_label = mark._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Наименование')

    def test_name_length(self):
        mark = models.CarMark.objects.get(id=1)
        max_length = mark._meta.get_field('name').max_length
        self.assertEquals(max_length, 50)

    def test_verbose_name_plural(self):
        mark = models.CarMark.objects.get(id=1)
        verbose_name_plural = mark._meta.verbose_name_plural
        self.assertEquals(verbose_name_plural, 'Марки')

    def test_object_name_is_name(self):
        mark = models.CarMark.objects.get(id=1)
        expected_object_name = mark.name
        self.assertEquals(expected_object_name, str(mark))


class CarModelModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        mark = models.CarMark.objects.create(name='LADA')
        models.CarModel.objects.create(name='GRANTA', mark=mark)

    def test_name_label(self):
        car_model = models.CarModel.objects.get(id=1)
        field_label = car_model._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Наименование')

    def test_name_max_length(self):
        car_model = models.CarModel.objects.get(id=1)
        max_length = car_model._meta.get_field('name').max_length
        self.assertEquals(max_length, 50)

    def test_mark_related_model(self):
        car_model = models.CarModel.objects.get(id=1)
        related_model = car_model._meta.get_field('mark').related_model
        self.assertEquals(related_model, models.CarMark)

    def test_mark_many_to_one(self):
        car_model = models.CarModel.objects.get(id=1)
        many_to_one = car_model._meta.get_field('mark').many_to_one
        self.assertTrue(many_to_one)

    def test_mark_label(self):
        car_model = models.CarModel.objects.get(id=1)
        field_label = car_model._meta.get_field('mark').verbose_name
        self.assertEquals(field_label, 'Марка')

    def test_verbose_name_plural(self):
        car_model = models.CarModel.objects.get(id=1)
        verbose_name_plural = car_model._meta.verbose_name_plural
        self.assertEquals(verbose_name_plural, 'Модели')

    def test_object_name_is_mark_and_name(self):
        car_model = models.CarModel.objects.get(id=1)
        expected_object_name = f'{car_model.mark} {car_model.name}'
        self.assertEquals(expected_object_name, str(car_model))


class CarModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        owner = models.Owner.objects.create(name='ТВП')
        car_mark = models.CarMark.objects.create(name='LADA')
        car_model = models.CarModel.objects.create(name='GRANTA', mark=car_mark)

        car = models.Car.objects.create(
            car_model=car_model,
            gos_number='P302MH31',
            owner=owner,
            mileage=5000,
            slug='p302mh31',
            year=2020,
            active=True
        )

        models.CarParam.objects.create(
            car_id=car.id,
            insurance='2025-11-25',
            technical_service=25000,
            grm=55000
        )

        models.Car.objects.create(
            car_model=car_model,
            gos_number='C302CA31',
            owner=owner,
            mileage=55400,
            slug='c302ca31',
            year=2022,
            active=False
        )

        user = User.objects.create_user(username='TEST')

        manager_models.DailyCheck.objects.create(
            car=car,
            author=user,
        )

    def setUp(self):
        self.car = models.Car.objects.get(id=1)
        self.user = models.User.objects.get(id=1)

    def test_verbose_name_plural(self):
        verbose_name_plural = self.car._meta.verbose_name_plural
        self.assertEquals(verbose_name_plural, 'Автомобили')

    def test_manager_free_cars(self):
        self.assertTrue(all(car.active for car in models.Car.free_cars.all()))

    def test_car_fields_related_model(self):
        def get_related_model(field_name):
            return self.car._meta.get_field(field_name).related_model

        car_model_related_model = get_related_model('car_model')
        self.assertEquals(car_model_related_model, models.CarModel)

        owner_related_model = get_related_model('owner')
        self.assertEquals(owner_related_model, models.Owner)

    def test_car_fields_label(self):
        def get_verbose_name(field_name):
            return self.car._meta.get_field(field_name).verbose_name

        car_model_field_label = get_verbose_name('car_model')
        self.assertEquals(car_model_field_label, 'Марка/Модель')

        gos_number_field_label = get_verbose_name('gos_number')
        self.assertEquals(gos_number_field_label, 'Гос. номер')

        owner_field_label = get_verbose_name('owner')
        self.assertEquals(owner_field_label, 'Владелец')

        mileage_field_label = get_verbose_name('mileage')
        self.assertEquals(mileage_field_label, 'Пробег')

        slug_field_label = get_verbose_name('slug')
        self.assertEquals(slug_field_label, 'SLUG-ссылка')

        year_field_label = get_verbose_name('year')
        self.assertEquals(year_field_label, 'Год выпуска')

        active_field_label = get_verbose_name('active')
        self.assertEquals(active_field_label, 'Статус')

    def test_car_fields_max_length(self):
        def get_max_length(field_name):
            return self.car._meta.get_field(field_name).max_length

        gos_number_max_length = get_max_length('gos_number')
        self.assertEquals(gos_number_max_length, 9)

        slug_max_length = get_max_length('slug')
        self.assertEquals(slug_max_length, 9)

    def test_fields_default(self):
        def get_default(field_name):
            return self.car._meta.get_field(field_name).default

        year_default = get_default('year')
        self.assertEquals(year_default, 2000)

        active_default = get_default('active')
        self.assertEquals(active_default, True)

    def test_field_year_count_validator(self):
        validators = self.car._meta.get_field('year').validators
        self.assertTrue(len(validators) == 2)

        min_validator, max_validator = validators
        self.assertEquals(min_validator.limit_value, 1950)
        self.assertEquals(max_validator.limit_value, now().year)

    def test_object_name_is_gos_number(self):
        object_name = self.car.gos_number
        self.assertEquals(object_name, str(self.car))

    def test_get_active_daily_check(self):
        active = self.car.get_active_daily_check().active
        self.assertTrue(active)

    def test_get_last_daily_check(self):
        last = manager_models.DailyCheck.objects.filter(car_id=self.car.id).order_by('-created').first()
        self.assertEquals(self.car.get_last_daily_check(), last)

    def test_get_now_daily_check(self):
        now_daily = manager_models.DailyCheck.objects.filter(car_id=self.car.id, created__day=now().day).first()
        self.assertEquals(self.car.get_now_daily_check().first(), now_daily)

    def test_get_absolute_url(self):
        self.assertEquals(self.car.get_absolute_url(), '/info_car/1')
