from django.urls import path
from . import views

app_name = 'influencers'

urlpatterns = [
    path('', views.influencer_list, name='list'),
    path('create/', views.create_profile, name='create_profile'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('portfolio/', views.portfolio_list, name='portfolio'),
    path('portfolio/add/', views.portfolio_add, name='portfolio_add'),
    path('portfolio/delete/<int:pk>/', views.portfolio_delete, name='portfolio_delete'),
    path('<int:pk>/', views.influencer_detail, name='detail'),
]