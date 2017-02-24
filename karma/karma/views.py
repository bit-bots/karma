from django.shortcuts import redirect
from django.template.response import TemplateResponse


def index(request):
    if request.user.is_authenticated:
        return redirect('karma_personal')
    return TemplateResponse(request, 'karma/index.html',
                            {}
                            )


def personal_page(request):
    return TemplateResponse(request, 'karma/personal.html', {})
