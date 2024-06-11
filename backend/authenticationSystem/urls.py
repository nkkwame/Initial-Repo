from django.urls import path
from .views import *

urlpatterns = [
    path('logout-account', logout_page, name='logout'),
    path('register/', register_user, name='register'),
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
]