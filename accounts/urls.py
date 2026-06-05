from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . import pages_views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('register/role/', views.role_select, name='role_select'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Password reset
    path('forgot-password/', auth_views.PasswordResetView.as_view(
        template_name='accounts/forgot_password.html',
        email_template_name='accounts/password_reset_email.html',
        subject_template_name='accounts/password_reset_subject.txt',
        success_url='/forgot-password/done/'
    ), name='forgot_password'),

    path('forgot-password/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/forgot_password_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html',
        success_url='/reset/done/'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),

    # Footer pages
    path('about/', pages_views.about, name='about'),
    path('contact/', pages_views.contact, name='contact'),
    path('faqs/', pages_views.faqs, name='faqs'),
    path('privacy/', pages_views.privacy, name='privacy'),
    path('terms/', pages_views.terms, name='terms'),
]