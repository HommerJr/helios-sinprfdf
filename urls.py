# -*- coding: utf-8 -*-
from django.conf import settings
from django.urls import include, re_path
from django.views.static import serve

from django.contrib import admin

admin.autodiscover()


urlpatterns = [
    re_path(r'^auth/', include('helios_auth.urls')),
    re_path(r'^helios/', include('helios.urls')),

    # SHOULD BE REPLACED BY APACHE STATIC PATH
    re_path(r'booth/(?P<path>.*)$', serve, {'document_root' : settings.BASE_DIR.__str__() + '/heliosbooth'}),
    re_path(r'verifier/(?P<path>.*)$', serve, {'document_root' : settings.BASE_DIR.__str__() + '/heliosverifier'}),

    re_path(r'static/helios_auth/(?P<path>.*)$', serve, {'document_root' : settings.BASE_DIR.__str__() + '/helios_auth/static/helios_auth'}),
    re_path(r'static/helios/(?P<path>.*)$', serve, {'document_root' : settings.BASE_DIR.__str__() + '/helios/static/helios'}),
    re_path(r'static/server_ui/(?P<path>.*)$', serve, {'document_root' : settings.BASE_DIR.__str__() + '/server_ui/static/server_ui'}),

    re_path(r'^', include('server_ui.urls')),

    re_path(r'^admin/', admin.site.urls),
]
