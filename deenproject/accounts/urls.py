from django.urls import path
from . import views
from .views import google_login_redirect, verify_email_view, profile_view


app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('google/redirect/', google_login_redirect, name='google_login_redirect'),
    path('verify-email/', verify_email_view, name='verify_email'),
    path('profile/', profile_view, name='profile'),
    path('resend-verification/', views.resend_verification_email, name='resend_verification_email'),
]
