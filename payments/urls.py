from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('history/', views.transaction_history, name='history'),
    path('<int:collab_pk>/', views.payment_overview, name='overview'),
    path('<int:collab_pk>/release/', views.release_payment, name='release'),
]