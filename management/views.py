from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse
from django.utils.timezone import now
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import DailyCheckForm
from .models import CarMigration, DailyCheck
from manual.models import Car, CarParam


@require_GET
def get_all_car(request):
    cars = Car.free_cars.all()

    context = {
        'cars': cars
    }

    return render(request,
                  template_name='management/cars_list.html',
                  context=context)


@require_GET
def create_car_migration(request, car_id):
    car = get_object_or_404(
        klass=Car,
        id=car_id,
        parameters__status=CarParam.Status.FREE
    )

    CarMigration.objects.create(car=car, author=request.user)

    messages.success(request, message=f'Вам назначен автомобиль {car}')

    return redirect(to=reverse(viewname='management:profile'))


@require_GET
def car_return(request, car_id):
    car_migration = get_object_or_404(
        CarMigration,
        car=car_id,
        author=request.user,
        active=True
    )

    car_parameters = car_migration.car.parameters

    car_parameters.status = CarParam.Status.FREE
    car_parameters.save()

    car_migration.active = False
    car_migration.save()

    return redirect(to=reverse(viewname='management:profile'))


@require_GET
def get_profile(request):
    user_cars = CarMigration.objects.filter(
        author=request.user,
        active=True
    ).values('car')

    cars = Car.objects.filter(id__in=user_cars)

    context = {
        'user': request.user,
        'cars': cars
    }

    return render(
        request=request,
        template_name='management/user_cars.html',
        context=context
    )


@require_GET
def create_daily_check(request, car_id):
    car_migration = get_object_or_404(
        CarMigration,
        car=car_id,
        author=request.user,
        active=True
    )

    car_migration.daily_check.create(
        car=car_migration.car,
        author=request.user
    )

    return redirect(to=reverse(viewname='management:profile'))


def close_daily_check(request, car_id):
    form = DailyCheckForm()

    if request.method == 'POST':
        daily_check = get_object_or_404(DailyCheck, car=car_id, active=True, author=request.user)

        form = DailyCheckForm(data=request.POST, instance=daily_check)
        if form.is_valid():
            form.instance.active = False
            form.save()

            return redirect(to=reverse(viewname='management:profile'))

    return render(request, template_name='management/close_daily_check.html', context={'form': form})


def redirect_view(request):
    response = redirect(reverse('management:car_list'))
    return response
