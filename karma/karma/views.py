from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models import Sum
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from django.template.response import TemplateResponse
from datetime import timedelta
import math
from django.utils.timezone import now
from django.core.paginator import Paginator

from karma.karma.forms import KarmaPointsForm, KarmaProjectForm, KarmaCategoryForm
from karma.karma.models import KarmaPoints, Project, Category
from django.conf import settings


def index(request):
    if request.user.is_authenticated:
        return redirect('karma_personal')
    return TemplateResponse(request, 'karma/index.html',
                            {}
                            )


@login_required()
def personal_page(request, point_id=None):
    if point_id:
        point_object = get_object_or_404(KarmaPoints, pk=point_id, user=request.user)
    else:
        point_object = None
    if request.POST:
        form = KarmaPointsForm(request.POST, instance=point_object)
        if form.is_valid():
            point = form.save(commit=False)
            point.user = request.user
            point.save()
            return redirect('karma_personal')
    else:
        form = KarmaPointsForm(instance=point_object)

    return TemplateResponse(request, 'karma/personal.html', {
        'edit': point_id,
        'form': form,
        'points': KarmaPoints.objects.filter(user=request.user).order_by('-time'),
        'sum': KarmaPoints.objects.filter(user=request.user).aggregate(Sum('points'))['points__sum'],
        'projects': Project.objects.filter(Q(user=request.user) | Q(group__user=request.user)).distinct().order_by('name'),
        'categories': Category.objects.filter(Q(project__user=request.user) | Q(project__group__user=request.user)).distinct().order_by('name'),
    })

@login_required()
def add_project(request):
    if request.POST:
        form = KarmaProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('karma_add_project')
    else:
        form = KarmaProjectForm()
    return TemplateResponse(request, 'karma/add_project.html', {
        'form': form,
        'projects': Project.objects.filter(Q(user=request.user) | Q(group__user=request.user)).distinct().order_by('name')
    })


@login_required()
def add_categories(request):
    if request.POST:
        form = KarmaCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('karma_add_categories')
    else:
        form = KarmaCategoryForm()
    return TemplateResponse(request, 'karma/add_category.html', {
        'form': form,
        'categories': Category.objects.filter(Q(project__user=request.user)| Q(project__group__user=request.user)).distinct().order_by('name')
    })


@login_required()
def project_overview(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if not Project.objects.filter(pk=project_id).filter(Q(user=request.user) | Q(group__user=request.user)):
        raise HttpResponseForbidden()

    items = KarmaPoints.objects.filter(project=project).order_by('-time')

    page = request.GET.get('page')
    paginator = Paginator(items, settings.ITEMS_PER_PAGE)
    displayedItems = paginator.get_page(page)

    return TemplateResponse(request, 'karma/project_overview.html', {
        'project': project,
        'sum': KarmaPoints.objects.filter(project=project).aggregate(Sum('points'))['points__sum'],
        'points': displayedItems
    })

@login_required()
def category_overview(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    return TemplateResponse(request, 'karma/category_overview.html', {
        'category': category,
        'sum': KarmaPoints.objects.filter(category=category).aggregate(Sum('points'))['points__sum'],
        'points': KarmaPoints.objects.filter(category=category).order_by('-time')
    })


@login_required()
def project_user(request, project_id, user_login):
    project = get_object_or_404(Project, pk=project_id)
    user = get_object_or_404(User, username=user_login)
    if not Project.objects.filter(pk=project_id).filter(Q(user=request.user) | Q(group__user=request.user)):
        raise HttpResponseForbidden()
    return TemplateResponse(request, 'karma/project_user.html', {
        'project': project,
        'user': user,
        'sum': KarmaPoints.objects.filter(project=project, user=user).aggregate(Sum('points'))['points__sum'],
        'points': KarmaPoints.objects.filter(project=project, user=user).order_by('-time')
    })


@login_required()
def project_highscore(request, project_id, nr_days):
    project = get_object_or_404(Project, pk=project_id)
    if not Project.objects.filter(pk=project_id).filter(Q(user=request.user) | Q(group__user=request.user)):
        raise HttpResponseForbidden()

    if int(nr_days) > 100000:
        nr_days = '100000'

    userpoints = KarmaPoints.objects.\
        filter(project=project, time__gte=now()-timedelta(days=int(nr_days))).\
        values('user__username').\
        annotate(points=Sum('points')).\
        order_by('-points')

    return TemplateResponse(request, 'karma/project_highscore.html', {
        'days': nr_days,
        'project': project,
        'users': userpoints,
    })


def api_project_user_count(request, project_id, nr_days):
    project = get_object_or_404(Project, pk=project_id)

    usercount = KarmaPoints.objects.\
        filter(project=project, time__gte=now()-timedelta(days=int(nr_days))).values('user').distinct().count()
    return TemplateResponse(request, 'karma/api_project_active', {
        'count': usercount,
    })


def api_project_activity_points(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    userpoints_week = KarmaPoints.objects.\
        filter(project=project, time__gte=now()-timedelta(days=7)).\
        values('user__username').\
        annotate(points=Sum('points'))
    userpoints_day = KarmaPoints.objects.\
        filter(project=project, time__gte=now()-timedelta(days=1)).\
        values('user__username').\
        annotate(points=Sum('points'))

    activepoints_list = dict()

    # Add week points and points of last day to weight the last day more
    for userp in userpoints_week:
        username = userp["user__username"]
        activepoints_list[username] = userp["points"]

    for userp in userpoints_day:
        username = userp["user__username"]
        activepoints_list[username] += userp["points"]

    activepoints = 0
    for username, points in activepoints_list.items():
        # Take logarithm of karma points to count more karma less
        log_points = math.log(points)
        # Take square root to weight persons stronger than points
        activepoints += math.sqrt(log_points)

    # Scale
    activepoints *= 200
    # Return integer
    activepoints = int(activepoints)
    return TemplateResponse(request, 'karma/api_project_active', {
        'count': activepoints,
    })


@login_required()
def karma_rules(request):
    return TemplateResponse(request, 'karma/rules.html', {
        'projects': Project.objects.filter(Q(user=request.user) | Q(group__user=request.user)).distinct().order_by('name'),
    })
