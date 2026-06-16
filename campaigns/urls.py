from django.urls import path
from . import views

app_name = 'campaigns'

urlpatterns = [
    path('', views.campaign_list, name='list'),
    path('create/', views.create_campaign, name='create'),
    path('my/', views.my_campaigns, name='my_campaigns'),
    path('saved/', views.saved_campaigns, name='saved_campaigns'),
    path('request/<int:influencer_pk>/', views.send_collab_request, name='send_request'),
    path('collab/<int:pk>/respond/', views.respond_collab, name='respond_collab'),
    path('<int:pk>/', views.campaign_detail, name='detail'),
    path('<int:pk>/apply/', views.apply_campaign, name='apply'),
    path('<int:pk>/edit/', views.edit_campaign, name='edit'),
    path('<int:pk>/delete/', views.delete_campaign, name='delete'),
    path('<int:pk>/status/', views.change_campaign_status, name='change_status'),
    path('<int:pk>/bookmark/', views.toggle_bookmark_campaign, name='bookmark'),
]