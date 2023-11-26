from django.urls import path
from django.contrib import admin
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('management/', include('management.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.views.generic import RedirectView
urlpatterns += [
    path('', RedirectView.as_view(url='/management/', permanent=True)),
    path('', include('management.urls')),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
