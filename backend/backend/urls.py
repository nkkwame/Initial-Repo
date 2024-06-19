from django.contrib import admin
from django.urls import path, include
from authenticationSystem import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name= 'index'),
    path('accounts/', include('authenticationSystem.urls')),
    path('payment/', include('paymentSystem.urls'))
]
