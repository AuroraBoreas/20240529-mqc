from django.http import HttpRequest, HttpResponse, FileResponse
from django.shortcuts import render, redirect
from .forms import AppUserRegisterForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import auth
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET

@require_GET
@cache_control(max_age=60 * 60 * 24, immutable=True, public=True)
def favicon(request: HttpRequest) -> HttpResponse:
    """
    Render the favicon image as an HTTP response.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: The HTTP response object containing the favicon image.
    """
    file = (settings.BASE_DIR / 'core/static/img/favicons/favicon.ico').open('rb')
    return FileResponse(file)

def register(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = AppUserRegisterForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, _('Your account has been created!'))
            return redirect('user:login')
    else:
        form = AppUserRegisterForm()
    return render(request, 'core/user/register.html', context={'form':form})

class AppUserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'core/user/login.html'
    success_message = _('You have been logged in')

@login_required
def logout(request: HttpRequest) -> HttpResponse:
    auth.logout(request)
    return render(request, 'core/user/logout.html')