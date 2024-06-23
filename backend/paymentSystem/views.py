from django.contrib.auth.decorators import login_required
from paystackapi.paystack import Paystack
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
import requests


key= settings.PAYSTACK_SECRET_KEY_LIVE
# Create your views here.

@login_required(login_url='login')
def pay(request):
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
    return render(request, 'pay/pay.html', context= {
        'response_carriers': list_ofc,
        'response_banks': list_ofb
    })

def IntiateMoMoTransaction(request):
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
    paystack= Paystack(secret_key=key)
    response_from_api= paystack.transaction.verify(transactionID)
    response= JsonResponse(response_from_api, safe= False)
    return response