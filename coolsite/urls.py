from django.contrib import admin
from django.urls import path, include
from coolsite import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from jobs.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("jobs.urls")),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = pageNotFound