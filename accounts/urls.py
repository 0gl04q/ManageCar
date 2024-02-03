from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('profile/', views.profile, name='profile'),
]