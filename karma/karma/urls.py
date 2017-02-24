from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', index, name='karma_index'),
    url(r'^personal$', personal_page, name='karma_personal'),
]
