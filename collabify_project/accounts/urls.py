from django.urls import path
from . import views
from . import pages_views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('register/role/', views.role_select, name='role_select'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    # Footer pages
    path('about/', pages_views.about, name='about'),
    path('contact/', pages_views.contact, name='contact'),
    path('faqs/', pages_views.faqs, name='faqs'),
    path('privacy/', pages_views.privacy, name='privacy'),
    path('terms/', pages_views.terms, name='terms'),
]