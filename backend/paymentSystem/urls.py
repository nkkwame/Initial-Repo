from django.urls import path
from . import views

urlpatterns = [
    path('', views.pay, name='payment-page'),
    path('intiate-Momo-transaction/', views.IntiateMoMoTransaction, name='make-momo-payment'),
    path('first-Momo-Transaction/submit-otp/', views.continueMoMoTransaction, name='submit-otp'),
    path('intiate-Bank-transaction/', views.IntiateBankTransaction, name='make-bank-payment'),
    path('verifyDeposite/<int:transactionID>/',views.verifyTransaction, name= 'verify-transaction'),
    path('transaction\'s-history/',views.transactionHistory, name= 'transaction-history'),
    path('successful-transaction/',views.successfulPayment, name= 'success'),
    path('pay-methods/',views.paymentMethod, name='pay-methods'),
]