from django.urls import path
from . import views

urlpatterns = [
    path('', views.pay, name='payment-page'),
    path('intiate-transaction/', views.IntiateTransaction, name='make-payment'),
    path('firstTransaction/submit-otp/', views.continueTransaction, name='submit-otp'),
    path('verify/<int:transactionID>/',views.verifyTransaction, name= 'verify-transaction'),
]