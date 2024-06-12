from django.urls import path
from .views import *

urlpatterns = [
    path('logout-account', logout_page, name= 'logout'),
    path('sign-in/', login_page, name= 'login'),
    path('register/', register_user, name= 'register'),
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
    path('password-reset/request/', passwordReset, name= 'password-reset-request'), #send mail
    path('password-reset/confirm/<str:uidb64>/<str:token>/', passwordResetConfirm, name= 'password-reset-confirm'), #verify token and redirect
    # path('password-reset/complete/', passwordResetComplete, name= 'password-reset-complete'), send mail on completion
    # path('password-reset/done/', passwordResetDone, name= 'password-reset-done'), show reset done page
    path('password-change/<str:id>/', passwordChange, name= 'password-change'),# change password
]