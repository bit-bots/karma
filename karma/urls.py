"""karma URL Configuration"""
from django.contrib import admin
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('karma/', include('karma.karma.urls')),
    path('', lambda req: redirect('karma_index'), name='index'),
    path('api/', include('karma.api.urls')),
    path('calibration/', include('karma.calibration.urls')),
    path("auth/openid/", include("simple_openid_connect.integrations.django.urls")),
]
