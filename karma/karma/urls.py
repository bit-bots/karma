from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', index, name='karma_index'),
    url(r'^personal$', personal_page, name='karma_personal'),
    url(r'^add_project$', add_project, name='karma_add_project'),
    url(r'^add_categories$', add_categories, name='karma_add_categories'),
    url(r'^category/([\d]+)$', category_overview, name='karma_category_overview'),
    url(r'^project/([\d]+)$', project_overview, name='karma_project_overview'),
    url(r'^project_highscore/([\d]+)/([\d]+)$', project_highscore, name='karma_project_highscore'),
    url(r'^project/([\d]+)/([a-zA-Z0-9\.]+)$', project_user, name='karma_project_user'),
    url(r'^api/project/([\d]+)/active_count/days/([a-zA-Z0-9]+)$', api_project_user_count, name='karma_api_project_user_count'),
    url(r'^api/project/([\d]+)/active_points/$', api_project_activity_points, name='karma_api_project_activity_count'),
    url(r'^personal/edit/(\d+)/$', personal_page, name="edit_points"),
    url(r'^project/rules/$', karma_rules, name="karma_rules"),
]
