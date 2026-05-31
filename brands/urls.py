from django.urls import path
from . import views

app_name = 'brands'

urlpatterns = [
    path('create/', views.create_profile, name='create_profile'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('bookmarks/', views.bookmarks_list, name='bookmarks'),
    path('bookmark/<int:influencer_pk>/', views.toggle_bookmark, name='toggle_bookmark'),
    path('<int:pk>/', views.brand_detail, name='detail'),
]