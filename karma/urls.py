"""karma URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^karma/', include('karma.karma.urls')),
    url(r'^$', lambda req: redirect('karma_index'), name='index'),
    path('api/', include('karma.api.urls')),
    path('calibration/', include('karma.calibration.urls')),
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    path("auth/openid/", include("simple_openid_connect.integrations.django.urls")),
]
