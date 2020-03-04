from django.urls import path

from . import views

app_name = 'calibration'

urlpatterns = [
    path('', views.calibration, name='calibration')
]
