from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('user/<int:user_id>/', views.file_report, name='file_report'),
]