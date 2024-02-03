from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include(arg=('management.urls', 'management'), namespace='management')),

    # path('manuals/', include(arg=('manual.urls', 'manual'), namespace='manual'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
