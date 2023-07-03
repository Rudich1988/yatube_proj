from django.urls import path

from .views import (EmailConfirm, PasswordChangeDone, PasswordChangeFormView,
                    PasswordResetComplete, PasswordResetConfView,
                    PasswordResetDoneView, PasswordResetFormView,
                    UserLoginView, UserRegistrationview, logoutview)

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('registration/', UserRegistrationview.as_view(), name='registration'),
    path('logout/', logoutview, name='logout'),
    path('email_confirm/<str:uidb64>/<str:token>/', EmailConfirm.as_view(), name='email_confirm'),
    path('password_reset_form/', PasswordResetFormView.as_view(), name='password_reset_form'),
    path('password_change_form/<int:pk>', PasswordChangeFormView.as_view(), name='password_change_form'),
    path('password_change_done/', PasswordChangeDone.as_view(), name='password_change_done'),
    path('password_reset_done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<str:uidb64>/<str:token>/', 
         PasswordResetConfView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', PasswordResetComplete.as_view(), name='password_reset_complete'),
]
