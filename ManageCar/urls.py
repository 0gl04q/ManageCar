from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('api/', include('management_api.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('', include(arg=('management.urls', 'management'), namespace='management')),
    path('summernote/', include('django_summernote.urls'))
    # path('manuals/', include(arg=('manual.urls', 'manual'), namespace='manual'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
