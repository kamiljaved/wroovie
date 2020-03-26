
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, re_path
from .views import *

urlpatterns = [

    path('register/', register, name='register'),
    path('settings/', settings, name='settings'),
    re_path(r'^email_verify/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', email_verify, name='email_verify'),

    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),

    path('user/<str:username>/upgrade/<int:current>', user_upgrade, name='user-upgrade'),
    re_path(r'^user_process_upgrade_instructor/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', user_process_upgrade_instructor, name='user_process_upgrade_instructor'),


    path('api/profile/<int:pk>/follow/', FollowAPIToggle.as_view(), name='profile-follow'),

    path('<str:username>', profile, name='profile'),

    # Added by Usman END
]
