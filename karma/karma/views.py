from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.template.response import TemplateResponse

from karma.karma.forms import KarmaPointsForm
from karma.karma.models import KarmaPoints


def index(request):
    if request.user.is_authenticated:
        return redirect('karma_personal')
    return TemplateResponse(request, 'karma/index.html',
                            {}
                            )


@login_required()
def personal_page(request):
    if request.POST:
        form = KarmaPointsForm(request.POST)
        if form.is_valid():
            point = form.save(False)
            point.user = request.user
            point.save()
            form = KarmaPointsForm()
    else:
        form = KarmaPointsForm()

    return TemplateResponse(request, 'karma/personal.html', {
        'form': form,
        'points': KarmaPoints.objects.filter(user=request.user)
    })
