from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from swipe.core import urls as core_urls
from swipe.core import views as core_views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from django.conf.urls import handler400, handler403, handler404, handler500

handler400 = core_views.bad_req
handler403 = core_views.perm_denied
handler404 = core_views.page_not_found
handler500 = core_views.server_error

urlpatterns = [
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^home/', include(core_urls)),
    url(r'^$', core_views.home),
    url(r'^favicon.ico$',
        RedirectView.as_view(
            url=staticfiles_storage.url('favicon.ico')),name="favicon"
    ),
    url(r'^authenticate/$', core_views.logi),
    url(r'^login/$', auth_views.login),
    url(r'^logout/$', core_views.logout_view),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
