from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('influencer/<int:pk>/', views.leave_review_influencer, name='review_influencer'),
    path('brand/<int:pk>/', views.leave_review_brand, name='review_brand'),
]