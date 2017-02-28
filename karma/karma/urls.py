from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', index, name='karma_index'),
    url(r'^personal$', personal_page, name='karma_personal'),
    url(r'^add_project$', add_project, name='karma_add_project'),
    url(r'^add_categories$', add_categories, name='karma_add_categories'),
    url(r'^project/([\d]+)$', project_overview, name='karma_project_overview'),
    url(r'^project/([\d]+)/([a-zA-Z0-9]+)$', project_user, name='karma_project_user'),
]
