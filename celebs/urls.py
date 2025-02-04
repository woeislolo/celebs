from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve

from debug_toolbar.toolbar import debug_toolbar_urls

from celebs import settings
from men.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('men.urls')),
    path('captcha/', include('captcha.urls')),
]

urlpatterns += debug_toolbar_urls()

handler404 = PageNotFound.as_view()


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})]
    urlpatterns += [re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})]
