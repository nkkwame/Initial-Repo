from django.urls import path
from . import views

urlpatterns = [
    path('', views.pay, name='payment-page'),
    path('intiate-Momo-transaction/', views.IntiateMoMoTransaction, name='make-momo-payment'),
    path('first-Momo-Transaction/submit-otp/', views.continueMoMoTransaction, name='submit-otp'),
    path('intiate-Bank-transaction/', views.IntiateBankTransaction, name='make-bank-payment'),
    path('verify/<int:transactionID>/',views.verifyTransaction, name= 'verify-transaction'),
]