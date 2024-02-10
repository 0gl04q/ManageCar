from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth.views import LoginView
from .forms import LoginForm


class CustomLoginView(LoginView):
    form_class = LoginForm


@require_http_methods(['GET', 'POST'])
@login_required
def profile(request):
    return render(request, template_name='registration/profile.html')
