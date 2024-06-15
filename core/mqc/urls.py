from django.urls import path
from . import views

app_name = 'mqc'

urlpatterns = [
    # path('', views.index, name='index'),
    path('favicon.ico/', views.favicon, name='favicon'),

    path('', views.dashboard, name='dashboard'),

    path('getJsonData/', views.getJsonData, name='getJsonData'),

    # path('dashboard/', views.dashboard, name='dashboard'),
    
    path('dataset/', views.MajorQualityCaseFilterListView.as_view(), name='dataset'),
    
    # path('list/', FilterView.as_view(model=models.Book, template_name='core/reviewform/report.html'), name='booklist'),
    
    path('api/', views.MajorQualityCaseListAPIView.as_view(), name='api'),

    path('case/<int:pk>/detail/', views.MajorQualityCaseDetailView.as_view(), name='detail'),
    
    path('case/create/', views.MajorQualityCaseCreateView.as_view(), name='create'),
    
    path('case/<int:pk>/delete/', views.MajorQualityCaseDeleteView.as_view(), name='delete'),

    path('case/<int:pk>/update/', views.MajorQualityCaseUpdateView.as_view(), name='update'),

    
]