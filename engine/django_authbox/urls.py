_A='frontend.urls'
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include,path
from django.utils.translation import gettext_lazy as _
from .views import redirect_service
urlpatterns=[path(_('secret-admin/'),admin.site.urls),path('',include('core.urls')),path('__debug__/',include('debug_toolbar.urls')),path('accounts/',include('allauth.urls')),path('ckeditor5/',include('django_ckeditor_5.urls'),name='ck_editor_5_upload_file')]
urlpatterns+=i18n_patterns(path('',redirect_service),path(_('dashboard')+'/',include('backend.urls')),path('<str:service_type>/<str:shortuuid>/',include(_A)),path('<str:service_type>/',include(_A)))
if settings.DEBUG:urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT);urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
else:urlpatterns+=staticfiles_urlpatterns()