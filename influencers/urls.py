from django.urls import path
from . import views

app_name = 'influencers'

urlpatterns = [
    path('', views.influencer_list, name='list'),
    path('create/', views.create_profile, name='create_profile'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('<int:pk>/', views.influencer_detail, name='detail'),
]