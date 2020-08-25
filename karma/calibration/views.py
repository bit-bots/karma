from datetime import timedelta, date
import random
import statistics

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render
from rest_framework.status import HTTP_400_BAD_REQUEST

from karma.karma.models import KarmaPoints, Project
from karma.calibration.forms import CalibrationForm
from karma.calibration.models import Calibration


@login_required
def calibration(request):
    if request.method == 'POST':
        form = CalibrationForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.user = request.user
            c.save()
            messages.success(request, 'Calibration submitted successfully')
        else:
            raise HttpResponseBadRequest()
    range_start = date.today() - timedelta(days=365)
    range_end = date.today()
    start = range_start + random.random() * (range_end - range_start)
    end = start + timedelta(days=7)
    project = Project.objects.get(id=settings.CALIBRATION_PROJECT)
    week_entries = KarmaPoints.objects. \
        filter(project=project, time__gte=start, time__lte=end + timedelta(days=1))
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

@login_required
def calibration_data(request):
    data = Calibration.objects.all()
    csv = ['week_points_sum,week_user_count,week_mean,week_median,week_stddev,day_points_sum,day_user_count,day_mean,day_median,day_stddev,calibration']
    for entry in data:
        start = entry.start_day
        end = entry.end_day
        project = Project.objects.get(id=settings.CALIBRATION_PROJECT)
        week_entries = KarmaPoints.objects. \
            filter(project=project, time__gte=start, time__lte=end + timedelta(days=1))
        week_points = week_entries. \
            values('user__username'). \
            annotate(points=Sum('points')).order_by('-points')
        week_points = [e['points'] for e in week_points]
        week_persons = len(week_points)
        if week_points:
            wmean = statistics.mean(week_points)
            wmedian = statistics.median(week_points)
            wpoints = sum(week_points)
        else:
            wmean = wmedian = wpoints = 0
        if len(week_points) > 1:
            wstdev = statistics.stdev(week_points)
        else:
            wstdev = 0

        day_entries = KarmaPoints.objects. \
            filter(project=project, time__day=end.day, time__month=end.month, time__year=end.year)
        day_points = day_entries. \
            values('user__username'). \
            annotate(points=Sum('points')). \
            order_by('-points')
        day_points = [e['points'] for e in day_points]
        day_persons = len(day_points)
        if day_points:
            dmean = statistics.mean(day_points)
            dmedian = statistics.median(day_points)
            dpoints = sum(day_points)
        else:
            dmean = dmedian = dpoints = 0
        if len(day_points) > 1:
            dstdev = statistics.stdev(day_points)
        else:
            dstdev = 0

        percentage = entry.percent / 100
        csv.append(','.join([str(x) for x in [wpoints, week_persons, wmean, wmedian, wstdev, dpoints, day_persons, dmean, dmedian, dstdev, percentage]]))
    return HttpResponse('\n'.join(csv), content_type='text/csv')
