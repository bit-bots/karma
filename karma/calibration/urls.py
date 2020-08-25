from django.urls import path

from . import views

app_name = 'calibration'

urlpatterns = [
    path('', views.calibration, name='calibration'),
    path('data', views.calibration_data, name='calibration_data')
]
