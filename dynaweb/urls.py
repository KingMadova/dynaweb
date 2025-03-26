from django.contrib import admin
from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('members/', include('django.contrib.auth.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('members/', include('members.urls')),
    path('forum/', include('forum.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
