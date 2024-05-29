from django.urls import path
from . import views

app_name = 'mailling'

urlpatterns = [
    path('send/', views.send_email_view, name='send'),
]