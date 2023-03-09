from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import re_path, include
from django.views.i18n import JavaScriptCatalog

urlpatterns = i18n_patterns(
    re_path(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog')
)

urlpatterns += staticfiles_urlpatterns()

urlpatterns += i18n_patterns(
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^', include('cms.urls'))
)

if settings.DEBUG:
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))

# the new django admin sidebar is bad UX in django CMS custom admin views.
admin.site.enable_nav_sidebar = False
