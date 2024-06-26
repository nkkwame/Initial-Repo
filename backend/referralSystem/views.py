from authenticationSystem.models import CustomUserModel as User
from django.shortcuts import render
from .models import *
import random, string

# Create your views here.

def pay_commission(referred_by_code, new_user_referral_code, commission_rate):
    referrer = User.objects.get(referral_code=referred_by_code)
    new_user = User.objects.get(referral_code=new_user_referral_code)

    referrer.points_earned += commission_rate

    #Check if referrer was also referred by someone
    if referrer.referred_by != '':
        referrer_referral = User.objects.get(referral_code=referrer.referred_by)
        referrer_referral.points_earned += round((commission_rate * 0.5), 1)
        if referrer_referral.indirect_referrals == '':
            referrer_referral.indrect_referrals += str(new_user.username)
        else:
            referrer_referral.indrect_referrals += ',' + str(new_user.username)
        referrer_referral.indirectReferrals += 1
        referrer_referral.save()
    referrer.save()

def new_referral(referred_by_code, new_user_referral_code):
    new_user = User.objects.get(referral_code=new_user_referral_code)
    referred_by= User.objects.get(referral_code=referred_by_code)

    pay_commission(referred_by_code, new_user_referral_code, 0.2)

    referred_by.referrals += 1
    if referred_by.direct_referrals == '':
        referred_by.direct_referrals += str(new_user.username)
    else:
        referred_by.direct_referrals += ',' + str(new_user.username)
    referred_by.save()

    new_user.referred_by = referred_by.referral_code
    new_user.save()

def generate_unique_referral_code(length=8, userName=None):
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for _ in range(length))

    while ReferralModel.objects.filter(referral_code=code).exists():
        code = ''.join(random.choice(characters) for _ in range(length))
    if userName:
        user= User.objects.get(username=userName)
        user_ref= ReferralModel.objects.create(referral_code= code, user= user)
        user_ref.save()

    return code
    
def referral_link(host, code):
    return f'{host}/accounts/referral/{code}'
