from datetime import timedelta, date
import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from rest_framework.status import HTTP_400_BAD_REQUEST

from karma.karma.models import KarmaPoints, Project
from karma.calibration.forms import CalibrationForm


@login_required
def calibration(request):
    if request.method == 'POST':
        form = CalibrationForm(request.POST)
        if form.is_valid():
            form.user = request.user
            form.save()
            messages.success(request, 'Calibration submitted successfully')
        else:
            raise HttpResponseBadRequest()
    range_start = date.today() - timedelta(days=365)
    range_end = date.today()
    start = range_start + random.random() * (range_end - range_start)
    end = start + timedelta(days=7)
    project = Project.objects.get(id=1)
    week_entries = KarmaPoints.objects. \
        filter(project=project, time__gte=start, time__lte=end)
    week_points = week_entries. \
        values('user__username'). \
        annotate(points=Sum('points')).order_by('-points')
    week_persons = len(week_points)
    day_entries = KarmaPoints.objects. \
        filter(project=project, time__day=end.day, time__month=end.month, time__year=end.year)
    day_points = day_entries. \
        values('user__username'). \
        annotate(points=Sum('points')). \
        order_by('-points')
    day_persons = len(day_points)
    form = CalibrationForm({'start_day': start, 'end_day': end})
    return render(request, 'calibration/calibration.html', {
        'form': form,
        'week_points': week_points,
        'week_persons': week_persons,
        'week_entries': week_entries.count(),
        'week_sum': week_entries.aggregate(Sum('points'))['points__sum'] or 0,
        'day_points': day_points,
        'day_persons': day_persons,
        'day_entries': day_entries.count(),
        'day_sum': day_entries.aggregate(Sum('points'))['points__sum'] or 0,
        'start_day': start,
        'end_day': end,
    })
