from authenticationSystem.models import CustomUserModel as User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from paystackapi.paystack import Paystack
from django.http import JsonResponse
from django.contrib import messages
from referralSystem.views import *
from django.conf import settings
from decimal import Decimal
from .models import *
import requests
import json


key= settings.PAYSTACK_SECRET_KEY_TEST
# Create your views here.

@login_required(login_url='login')
def pay(request):
    if not request.user.is_premium:
        headers = {
        'Authorization': f'Bearer {key}'
    }
        list_of_carriers= requests.get(url='https://api.paystack.co/bank?currency=GHS&type=mobile_money', headers= headers)
        list_of_banks= requests.get(url='https://api.paystack.co/bank?country=ghana&pay_with_bank=true', headers= headers)
        response_carriers= list_of_carriers.json()
        response_banks= list_of_banks.json()
        list_ofc= []
        list_ofb= []
        for i in response_carriers['data']:
            list_ofc.append(i)
        for i in response_banks['data']:
            list_ofb.append(i)
        return render(request, 'pay/pay.html')
    else:
        messages.error(request, 'You are already a premium user')
        return redirect('index')

def IntiateMoMoTransaction(request):
    if not request.user.is_premium:
        if request.method == 'POST':
            email= request.POST.get('email')
            phone= request.POST.get('phone')
            amount= request.POST.get('amount')
            carrier= request.POST.get('carrier')

            headers = {
                            'Authorization': f'Bearer {key}',
                            'Content-Type': 'application/json'
                        }

            url = 'https://api.paystack.co/charge'
            params = {
                        "amount": float(amount) * 100,
                        "email": email,
                        "currency": "GHS",
                        "mobile_money": {
                            "phone": phone,
                            "provider": carrier,
                        }
                    }
            make_a_charge= requests.post(url, headers={
                            'Authorization': f'Bearer {key}',
                            'Content-Type': 'application/json'
                        }, json=params)
            response= make_a_charge.json()
            return JsonResponse(response, safe= False)
    else:
        messages.error(request, 'You are already a premium user')
        return redirect('index')

def continueMoMoTransaction(request):
    if request.method == 'POST':
        opt_code= request.POST.get('opt_code')
        ref_code= request.POST.get('ref_code')

        url="https://api.paystack.co/charge/submit_otp"
        data={ 
        "otp": opt_code, 
        "reference": ref_code,
        }

        continue_charge= requests.post(url, headers={
                        'Authorization': f'Bearer {key}',
                        'Content-Type': 'application/json'
                    }, json=data)
        response= continue_charge.json()
        return JsonResponse(response, safe= False)

def IntiateBankTransaction(request):
    if request.method == 'POST':
        acN= request.POST.get('accountNumber')
        dob= request.POST.get('dob')
        amount= request.POST.get('amount')
        bank= request.POST.get('bank')
        url="https://api.paystack.co/charge"
        data={ 
            "email": str(request.user.email),
            "amount": str(amount),
            "bank": {
                'code': str(bank),
                'account_number': str(acN)
                },
            }

        continue_charge= requests.post(url, headers={
                        'Authorization': f'Bearer {key}',
                        'Content-Type': 'application/json'
                    }, json=data)
        response= continue_charge.json()
        return JsonResponse(response, safe= False)

def verifyTransaction(request, transactionID):
    if not request.user.is_premium:
        user= User.objects.get(email=request.user.email)
        transactionExist= False
        paystack= Paystack(secret_key=key)
        response_from_api= paystack.transaction.verify(str(transactionID))
        if response_from_api['message'] == "Transaction reference not found":
            messages.error(request, 'Transaction not found')
            return redirect('index')
        elif response_from_api['message'] != "Transaction reference not found":
            reflist= TransactionModel.objects.filter(transactionRefrence= response_from_api['data']['reference'])
            for transaction in reflist:
                if transaction.account.user.email == request.user.email:
                    transactionExist= True
                    break
            if transactionExist:
                messages.error(request, 'Transaction already made')
                return redirect('index')
            else:
                try:
                    account= AccountModel.objects.get(user= user)
                except AccountModel.DoesNotExist:
                    account= AccountModel.objects.create(user= user)
                    account.save()
                amount= Decimal(response_from_api['data']['amount'] / 100)
                transactionType= 'deposit'
                transactionTypeStatus= response_from_api['data']['status']
                transactionRefrence= response_from_api['data']['reference']
                paymentMethod= response_from_api['data']['channel']
                mobileNumber= response_from_api['data']['authorization']['mobile_money_number']
                carrier= response_from_api['data']['authorization']['bank']
                transaction_made= TransactionModel.objects.create(
                    account= account,
                    amount= amount,
                    transactionType= transactionType,
                    transactionTypeStatus= transactionTypeStatus,
                    transactionRefrence= transactionRefrence,
                    paymentMethod= paymentMethod,
                    mobileNumber= mobileNumber,
                    carrier= carrier
                )
                transaction_made.save()
                if response_from_api['data']['status'] == 'success':
                    account.make_PremiumUser()
                    user.referral_code= generate_unique_referral_code(userName= user.username)
                    user.save()
                    userPaymentMethod= PaymentInfoModel.objects.create(
                        account= user,
                        paymentMethod= paymentMethod,
                        accountNumber= mobileNumber,
                        carrier= carrier,
                        firstName= user.first_name,
                        lastName= user.last_name,
                        email= user.email
                    )
                    userPaymentMethod.save()
                    if user.referred_by != '':
                        new_referral(user.referred_by, user.referral_code)
    else:
        messages.error(request, 'You are already a premium user')
        return redirect('index')

    response= JsonResponse(response_from_api, safe= False)
    return response

def successfulPayment(request):
    return render(request, 'pay/paymentSuccess.html')

@login_required(login_url='login')
def transactionHistory(request):
    if request.user.is_premium:
        try:
            account= AccountModel.objects.get(user= User.objects.get(email=request.user.email))
        except AccountModel.DoesNotExist:
            return redirect('index')
        transactions= TransactionModel.objects.filter(account= account)
        return render(request, 'pay/transactionHistory.html', context= {
            'transactions': transactions,
        })
    else:
        messages.error(request, 'You are not a premium user. Please upgrade to continue.')
        return redirect('index')
    
def paymentMethod(request):
    if request.user.is_premium:
        if request.method == 'POST':
            user= User.objects.get(email=request.user.email)
            userPaymentMethod= PaymentInfoModel.objects.get(account= user)
            first_name= request.POST.get('fn')
            last_name= request.POST.get('ln')
            email= request.POST.get('ea')
            accountNumber= request.POST.get('mn')
            carrier= request.POST.get('network-carriers')
            paymentMethod= request.POST.get('paym')

            userPaymentMethod.firstName= first_name
            userPaymentMethod.lastName= last_name
            userPaymentMethod.email= email
            userPaymentMethod.accountNumber= accountNumber
            userPaymentMethod.carrier= carrier
            userPaymentMethod.paymentMethod= paymentMethod
            userPaymentMethod.save()
            messages.success(request, 'Payment method updated successfully')
            return redirect('index')


        headers = {
        'Authorization': f'Bearer {key}'
        }
        list_of_carriers= requests.get(url='https://api.paystack.co/bank?currency=GHS&type=mobile_money', headers= headers)
        response_carriers= list_of_carriers.json()
        list_ofc= []
        for i in response_carriers['data']:
            list_ofc.append(i)
        userPaymentMethod= PaymentInfoModel.objects.get(account= User.objects.get(email= request.user.email))
        print(userPaymentMethod.accountNumber)
        context= {
            'first_name': userPaymentMethod.firstName,
            'last_name': userPaymentMethod.lastName,
            'email': userPaymentMethod.email,
            'phone': userPaymentMethod.accountNumber,
            'carrier': userPaymentMethod.carrier,
            'paymentMethod': userPaymentMethod.paymentMethod,
            'paymentMethodName': userPaymentMethod.paymentMethodName,
            'otherCarriers': list_ofc,
            'otherpaymentMethods': PaymentChannels.objects.all(),
        }
        return render(request, 'pay/paymentMethod.html', context= context)
    else:
        messages.error(request, 'You are not a premium user. Please upgrade to continue.')
        return redirect('index')