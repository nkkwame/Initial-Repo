from django.urls import path
from .views import *

urlpatterns = [
    path('logout-account', logout_page, name= 'logout'),
    path('sign-in/', login_page, name= 'login'),
    path('register/', register_user, name= 'register'),
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
    path('password-reset/', passwordReset, name= 'password-reset'),
]