from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

router = DefaultRouter()
router.register(r'karma', views.KarmaViewSet, basename='karma')
router.register(r'projects', views.ProjectViewSet, basename='projects')
urlpatterns = router.urls

urlpatterns += [
    path('auth/', obtain_auth_token),
]
