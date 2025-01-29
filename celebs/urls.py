from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve

from celebs import settings
from men.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('men.urls')),
    path('captcha/', include('captcha.urls')),
]


# handler404='men.views.page_not_found'
handler404 = PageNotFound.as_view()


if settings.DEBUG:
    import debug_toolbar  # импортируется только в дебаге, если вынести выше, не сработает

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls)),]
else:
    urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})]
    urlpatterns += [re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})]
