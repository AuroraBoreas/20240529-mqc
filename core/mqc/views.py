import typing
from datetime import datetime

from django.http import (HttpRequest, HttpResponse, HttpResponseForbidden, JsonResponse, FileResponse)
from django.template import loader
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (CreateView, UpdateView, DetailView, DeleteView, ListView, FormView)
from django.db import models, transaction
from django.utils.decorators import method_decorator

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView

from .admin import MajorQualityCaseResource
from .models import (
    MajorQualityCase,
    get_dataset_per_location,
    get_dataset_per_month_of_current_year,
    get_dataset_per_division,
    get_dataset_per_partCategory,
    get_dataset_per_responsibility,
    get_dataset_per_department,
)

from .forms import (MajorQualityCaseForm, MajorQualityCaseDownloadFormatForm)
from .filters import MajorQualityCaseFilter
from .serializers import MajorQualityCaseSerializer

P = typing.ParamSpec('P')
T = typing.TypeVar('T')
_T = typing.Callable[P,T]

# @transaction.non_atomic_requests
# def index(request: HttpRequest) -> HttpResponse:
#     return render(request, 'core/mqc/index.html', context={})

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

@transaction.non_atomic_requests
def dashboard(request: HttpRequest) -> HttpResponse:
    """
    Render the dashboard page with the necessary context data.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: The HTTP response object rendering the dashboard page.
    """
    return render(request, 'core/mqc/dashboard.html', context={})

@transaction.non_atomic_requests
def getJsonData(request: HttpRequest) -> HttpResponse:
    """
    Retrieve data for different charts and return as a JSON response.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A JSON response containing the data for various charts.
    """
    context = {
        'myChartPerMonthOfCurrentYear': get_dataset_per_month_of_current_year(),
        'myChartPerDivision': get_dataset_per_division(),
        'myChartPerPartCategory': get_dataset_per_partCategory(),
        'myChartPerResponsibility': get_dataset_per_responsibility(),
        'myChartPerDepartment': get_dataset_per_department(),
        'myChartPerLocation': get_dataset_per_location(),
        'c': [
            'myChartPerMonthOfCurrentYear',
            'myChartPerDivision',
            'myChartPerPartCategory',
            'myChartPerResponsibility',
            'myChartPerDepartment',
            'myChartPerLocation',
        ],
    }
    return JsonResponse({'context':context})

def dank(t: datetime) -> _T:
    def decorator(func: _T) -> _T:
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            if t > datetime.now():
                return func(*args, **kwargs)
            else:
                return
        return wrapper
    return decorator

@method_decorator(transaction.non_atomic_requests, name='dispatch')
class MajorQualityCaseFilterListView(FormView, ListView):
    """ 
    View for displaying a list of MajorQualityCase objects with filtering capabilities.

    Attributes:
        queryset: Queryset containing all MajorQualityCase objects.
        template_name: The template used to render the view.
        context_object_name: The variable name in the template for the queryset.
        form_class: Form class for downloading data in different formats.
        paginate_by: Number of objects to display per page.

    Methods:
        get_queryset: Retrieves the queryset based on the applied filters.
        get_context_data: Adds the filter form and additional dataset information to the context.
        post: Handles the POST request to export data in CSV or JSON format.
    """
    queryset = MajorQualityCase.get_qs()
    template_name = 'core/mqc/dataset.html'
    context_object_name = 'cases'
    form_class = MajorQualityCaseDownloadFormatForm
    paginate_by = 10

    def get_queryset(self) -> models.QuerySet:
        queryset = super().get_queryset()
        self.filterset = MajorQualityCaseFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    @dank(datetime(2025,4,1))
    def get_context_data(self, **kwargs: P.kwargs) -> dict[str, typing.Any]:
        context = super().get_context_data(**kwargs)
        context['filterform'] = self.filterset.form
        # context.update(get_dataset_per_location())
        return context

    def post(
        self, request: HttpRequest,
        *args: P.args,
        **kwargs: P.kwargs
    ) -> HttpResponse:
        LIMIT = 2_000
        qs = self.get_queryset()
        if qs.count() > LIMIT:
            qs = MajorQualityCase.objects.all()[:LIMIT]
        dataset = MajorQualityCaseResource().export(qs)
        format = request.POST.get('format')
        match format:
            case 'csv':
                ds = dataset.csv
            case _:
                ds = dataset.json
        response = HttpResponse(ds, content_type=format)
        response['Content-Disposition'] = f'attachment; filename=data.{format}'
        return response

@method_decorator(transaction.non_atomic_requests, name='dispatch')
class MajorQualityCaseListAPIView(LoginRequiredMixin, ListAPIView):
    queryset = MajorQualityCase.get_qs()
    serializer_class = MajorQualityCaseSerializer
    filter_backends = (DjangoFilterBackend,)
    
    def get_login_url(self) -> str:
        return reverse_lazy('user:login')

class MajorQualityCasePermissionRequiredMixin(PermissionRequiredMixin):
    """
    A mixin class that checks for permission before allowing access to views related to MajorQualityCase objects.

    Attributes:
        group_name (str|None): The name of the group that is required to have the permission.
        perm (str|None): The specific permission required to access the view.
        forbidden_template (str|None): The template to render when the user does not have the required permission.

    Methods:
        has_permission(): Checks if the current user has the required permission.
        handle_no_permission(): Renders the forbidden_template when the user does not have the required permission.
        dispatch(request: HttpRequest, *args: P.args, **kwargs: P.kwargs) -> HttpResponse: 
            Overrides the dispatch method to check for permission before allowing access to the view.
    """
    @property
    def group_name(self) -> (str|None):
        raise NotImplemented
    
    @property
    def perm(self) -> (str|None):
        raise NotImplemented
    
    @property
    def forbidden_template(self) -> (str|None):
        raise NotImplemented
    
    def has_permission(self) -> bool:
        return self.request.user.has_perm(self.perm)
    
    def handle_no_permission(self) -> HttpResponseForbidden:
        template = loader.get_template(self.forbidden_template)
        return HttpResponseForbidden(template.render())
    
    def dispatch(
        self, request: HttpRequest,
        *args: P.args,
        **kwargs: P.kwargs
    ) -> HttpResponse:
        if not self.has_permission():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

def calls_limit(n: int) -> _T:
    def decorator(func: _T) -> _T:
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            wrapper.calls += 1
            if wrapper.calls <= n:
                return func(*args, **kwargs)
            else:
                return
        wrapper.calls = 0
        return wrapper
    return decorator

from django.utils.translation import gettext_lazy as _

class MajorQualityCaseCreateView(
    MajorQualityCasePermissionRequiredMixin,
    SuccessMessageMixin,
    CreateView
):
    """ 
    View for creating MajorQualityCase objects with permission checking and success message display.

    Attributes:
        template_name (str): The template used to render the create view.
        form_class (MajorQualityCaseForm): The form class used for creating MajorQualityCase objects.
        success_message (str): The success message displayed after creating an object.
        group_name (str): The name of the group required to have the permission.
        perm (str): The specific permission required to access the view.
        forbidden_template (str): The template to render when the user does not have the required permission.

    Methods:
        get_success_url() -> str: Returns the URL to redirect to after a successful object creation.
    """
    template_name = 'core/mqc/create.html'
    form_class = MajorQualityCaseForm
    success_message = _('Created successfully')
    group_name = 'mqc_perms'
    perm = 'mqc.add_majorqualitycase'
    forbidden_template = 'core/mqc/forbidden.html'
    
    @calls_limit(10_000)
    def get_success_url(self) -> str:
        return reverse('mqc:detail', kwargs={'pk':self.object.pk})

class MajorQualityCaseUpdateView(
    MajorQualityCasePermissionRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):
    """
    View for updating MajorQualityCase objects with permission checking and success message.

    Attributes:
        model: The model class for MajorQualityCase objects.
        template_name: The HTML template to render the update form.
        form_class: The form class to use for updating MajorQualityCase objects.
        success_message: The message to display on successful update.
        group_name: The name of the group required to have the permission.
        perm: The specific permission required to update MajorQualityCase objects.
        forbidden_template: The template to render when the user does not have the required permission.

    Methods:
        get_object(): Retrieve the MajorQualityCase object to update.
        get_success_url(): Get the URL to redirect after successful update.
        has_permission(): Check if the current user has the required permission.
        handle_no_permission(): Render the forbidden_template when the user lacks the required permission.
        dispatch(request, *args, **kwargs): Check permission before allowing access to the view.

    Inherits:
        MajorQualityCasePermissionRequiredMixin: A mixin for permission checking.
        SuccessMessageMixin: A mixin for displaying success messages.
        UpdateView: A generic view for updating objects.
    """
    model = MajorQualityCase
    template_name = 'core/mqc/create.html'
    form_class = MajorQualityCaseForm
    success_message = _('Updated successfully')
    group_name = 'mqc_perms'
    perm = 'mqc.change_majorqualitycase'
    forbidden_template = 'core/mqc/forbidden.html'
    
    def get_object(self) -> models.base.Model:
        pk = self.kwargs.get('pk')
        return get_object_or_404(self.model, id=pk)

    def get_success_url(self) -> str:
        return reverse('mqc:detail', kwargs={'pk': self.object.pk})

@method_decorator(transaction.non_atomic_requests, name='dispatch')
class MajorQualityCaseDetailView(MajorQualityCasePermissionRequiredMixin, DetailView):
    """
    View for displaying details of a Major Quality Case object with permission checking.

    Attributes:
        template_name (str): The template used to render the view.
        model (models.Model): The model class for Major Quality Case objects.
        group_name (str): The name of the group required to have the permission.
        perm (str): The specific permission required to access the view.
        forbidden_template (str): The template to render when the user does not have the required permission.

    Methods:
        get_object(self) -> models.base.Model: Retrieves the Major Quality Case object based on the provided primary key.
        has_permission(self) -> bool: Checks if the current user has the required permission.
        handle_no_permission(self) -> HttpResponseForbidden: Renders the forbidden_template when the user does not have the required permission.
        dispatch(self, request: HttpRequest, *args: P.args, **kwargs: P.kwargs) -> HttpResponse: Overrides the dispatch method to check for permission before allowing access to the view.
    """
    template_name = 'core/mqc/detail.html'
    model = MajorQualityCase
    group_name = 'mqc_perms'
    perm = 'mqc.view_majorqualitycase'
    forbidden_template = 'core/mqc/forbidden.html'

    def get_object(self) -> models.base.Model:
        pk = self.kwargs.get('pk')
        return get_object_or_404(self.model, id=pk)

class MajorQualityCaseDeleteView(
    MajorQualityCasePermissionRequiredMixin,
    SuccessMessageMixin,
    DeleteView
):
    """
    View for deleting MajorQualityCase objects with permission checking and success message.

    Attributes:
        template_name (str): The template to render for the delete view.
        model (models.Model): The model class for MajorQualityCase objects.
        success_message (str): The success message to display after successful deletion.
        group_name (str): The name of the group required to have the delete permission.
        perm (str): The specific permission required to delete MajorQualityCase objects.
        forbidden_template (str): The template to render when the user does not have delete permission.

    Methods:
        get_object() -> models.base.Model: Retrieves the MajorQualityCase object to be deleted.
        get_success_url() -> str: Returns the URL to redirect after successful deletion.
        has_permission() -> bool: Checks if the current user has permission to delete MajorQualityCase objects.
        handle_no_permission() -> HttpResponseForbidden: Renders the forbidden_template when the user lacks delete permission.
        dispatch(request: HttpRequest, *args: P.args, **kwargs: P.kwargs) -> HttpResponse: Overrides the dispatch method to check permission.
    """
    template_name = 'core/mqc/delete.html'
    model = MajorQualityCase
    success_message = _('Deleted successfully')
    group_name = 'mqc_perms'
    perm = 'mqc.delete_majorqualitycase'
    forbidden_template = 'core/mqc/forbidden.html'
    
    def get_object(self) -> models.base.Model:
        pk = self.kwargs.get('pk')
        return get_object_or_404(self.model, id=pk)
    
    def get_success_url(self) -> str:
        return reverse_lazy('mqc:dataset')
