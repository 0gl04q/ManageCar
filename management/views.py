from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import DetailView, ListView
from django.views.decorators.http import require_GET, require_http_methods

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
import base64
from .forms import DailyCheckForm
from .models import CarMigration, DailyCheck
from manual.models import Car, CarParam, Photo
from manual.forms import CarForm, CarParametersForm
from django.core.files.base import ContentFile


@require_GET
@login_required
def get_all_car(request):
    cars = Car.free_cars.all()

    context = {
        'cars': cars
    }

    return render(request,
                  template_name='management/driver/change_cars.html',
                  context=context)


@require_GET
@login_required
def create_car_migration(request, car_id):
    car = get_object_or_404(
        klass=Car,
        id=car_id,
        parameters__status=CarParam.Status.FREE
    )

    CarMigration.objects.create(car=car, author=request.user)

    messages.success(request, message=f'Вам назначен автомобиль {car}')

    return redirect(to=reverse(viewname='management:user_cars'))


@require_GET
@login_required
def car_return(request, car_id):
    car_migration = get_object_or_404(
        CarMigration,
        car=car_id,
        author=request.user,
        active=True
    )

    car_migration.active = False
    car_migration.save()

    messages.success(request, message=f'Вы вернули {car_migration.car}')
    return redirect(to=reverse(viewname='management:user_cars'))


@require_GET
@login_required
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
        template_name='management/driver/user_cars.html',
        context=context
    )


@require_GET
@login_required
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

    car_migration.car.parameters.status = CarParam.Status.JOB
    car_migration.car.parameters.save()

    messages.success(request, message=f'Смена {car_migration.car} открыта!')

    return redirect(to=reverse(viewname='management:user_cars'))


@require_http_methods(('GET', 'POST'))
@login_required
def close_daily_check(request, daily_check_id):
    form = DailyCheckForm()
    daily_check = get_object_or_404(DailyCheck, id=daily_check_id)

    if request.method == 'POST':

        form = DailyCheckForm(request.POST, request.FILES, instance=daily_check)
        if form.is_valid():
            form.instance.active = False
            form.save()

            photo_1 = form.cleaned_data['photo_1']
            daily_check.photo.create(
                name=f'cбоку',
                file=photo_1,
                author=request.user
            )

            photo_2 = form.cleaned_data['photo_2']
            daily_check.photo.create(
                name=f'спереди',
                file=photo_2,
                author=request.user
            )

            car = daily_check.car
            car.mileage = form.cleaned_data['mileage_auto']
            car.save()

            messages.success(request, message=f'Cмена {car} закрыта!')

            return redirect(to=reverse(viewname='management:user_cars'))

    context = {
        'form': form,
        'daily_check_id': daily_check_id
    }

    return render(request, template_name='management/driver/close_daily_check.html', context=context)


def redirect_view(request):
    response = redirect(reverse('management:user_cars'))

    return response


class DirectorPermissionRequiredMixin(LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = 'manual.view_all_cars'
    raise_exception = True


class CarListView(DirectorPermissionRequiredMixin, ListView):
    queryset = Car.objects.all().order_by('parameters__status')
    context_object_name = 'cars'
    template_name = 'management/director/all_cars.html'


class CarDetailView(DirectorPermissionRequiredMixin, DetailView):
    model = Car
    context_object_name = 'car'
    template_name = 'management/director/info_car.html'


class DailyCheckDetailView(DirectorPermissionRequiredMixin, DetailView):
    model = DailyCheck
    context_object_name = 'daily_check'
    template_name = 'management/director/daily_check.html'


class CarDailyCheckListView(DirectorPermissionRequiredMixin, ListView):
    context_object_name = 'list_daily_check'
    template_name = 'management/director/list_car_daily_check.html'

    def get_queryset(self):
        return DailyCheck.objects.filter(car=self.kwargs['pk'])


@login_required
@permission_required(perm='manual.view_all_cars', raise_exception=True)
def edit_car(request, pk):
    car = get_object_or_404(Car, pk=pk)

    if request.method == 'POST':
        car_form = CarForm(request.POST, instance=car)
        car_parameters_form = CarParametersForm(request.POST, instance=car.parameters)

        if car_form.is_valid() and car_parameters_form.is_valid():
            car_form.save()
            car_parameters_form.save()
            messages.success(request, 'Изменения сохранены')
            return redirect(to='management:info_car', pk=pk)
    else:
        car_form = CarForm(instance=car)
        car_parameters_form = CarParametersForm(instance=car.parameters)

    context = {
        'car': car,
        'car_form': car_form,
        'car_parameters_form': car_parameters_form
    }

    return render(request, template_name='management/director/edit_car.html', context=context)


@login_required
@permission_required(perm='manual.view_all_cars', raise_exception=True)
def create_car(request):
    if request.method == 'POST':
        car_form = CarForm(request.POST)
        car_parameters_form = CarParametersForm(request.POST)

        if car_form.is_valid() and car_parameters_form.is_valid():
            car = car_form.save()

            car_parameters_form.instance.car = car
            car_parameters_form.save()

            messages.success(request, 'Автомобиль добавлен')

            return redirect(to='management:info_car', pk=car_form.instance.pk)
    else:
        car_form = CarForm()
        car_parameters_form = CarParametersForm()

    context = {
        'car_form': car_form,
        'car_parameters_form': car_parameters_form
    }

    return render(request, template_name='management/director/create_car.html', context=context)


@login_required
@permission_required(perm='manual.view_all_cars', raise_exception=True)
def update_ts(request, pk):
    parameters = get_object_or_404(Car, pk=pk).parameters
    parameters.technical_service = parameters.car.mileage + 10000
    parameters.save()
    return redirect(to='management:info_car', pk=pk)


@login_required
@permission_required(perm='manual.view_all_cars', raise_exception=True)
def update_grm(request, pk):
    parameters = get_object_or_404(Car, pk=pk).parameters
    parameters.grm = parameters.car.mileage + 30000
    parameters.save()
    return redirect(to='management:info_car', pk=pk)
