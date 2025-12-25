from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
     path('password_reset/', PasswordResetView.as_view(
        template_name='account/password_reset.html',
        email_template_name='account/password_reset_email.html',
        subject_template_name='account/password_reset_subject.txt',
        success_url='/login/'), name='password_reset'
    ),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('account/profile/', views.profile, name='profile'),
    path('account/update_profile/', views.update_profile, name='update_profile'),
]