from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='karma_index'),
    path('personal', personal_page, name='karma_personal'),
    path('add_project', add_project, name='karma_add_project'),
    path('add_categories', add_categories, name='karma_add_categories'),
    path('category/<int:category_id>', category_overview, name='karma_category_overview'),
    path('project/<int:project_id>', project_overview, name='karma_project_overview'),
    path('project_highscore/<int:project_id>/<int:nr_days>', project_highscore, name='karma_project_highscore'),
    path('project/<int:project_id>/<str:user_login>', project_user, name='karma_project_user'),
    path('api/project/<int:project_id>/active_count/days/<int:nr_days>', api_project_user_count, name='karma_api_project_user_count'),
    path('api/project/<int:project_id>/active_points/', api_project_activity_points, name='karma_api_project_activity_count'),
    path('personal/edit/<int:point_id>/', personal_page, name="edit_points"),
    path('project/rules/', karma_rules, name="karma_rules"),
]
