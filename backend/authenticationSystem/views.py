from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
# from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.models import User, auth 
# from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.contrib import messages
from paymentSystem.models import *
from django.conf import settings
from django.urls import reverse
from .tokensGenerator import *
from .models import *
from .forms import *

# Create your views here.
# @login_required(login_url='login')
def index(request):
    messages_to_display= messages.get_messages(request)
    userAccountType= 'Non-Premium User'
    userAccountBalance= 0
    try:
        if request.user.is_authenticated:
            userAccount= AccountModel.objects.get(user=request.user)
            if request.user.is_premium:
                userAccountType= 'Premium User'
            userAccountBalance= userAccount.balance
        else:
            pass
    except AccountModel.DoesNotExist:
        pass

    return render(request, 'index.html', context= {
        'messages': messages_to_display,
        'isPremium': {
            'accountType': userAccountType,
            'accountBalance': userAccountBalance
        },
    })

def register_user(request):
    messages_to_display= messages.get_messages(request)
    form= RegistrationForm()
    if request.method == 'POST':
        form= RegistrationForm(request.POST)
        if form.is_valid():
            to_email= form.cleaned_data.get('email')
            username= form.cleaned_data.get('username')
            user= form.save(commit= False)
            user.is_active= False
            user.save()
            current_site= get_current_site(request) #Geting the curent site domain
            token= TokenGeneratorValidator.make_token(user) #Generating hash 
            tokenID= TokensModel.objects.create(token=token, user_id=user.id) # Registering token to database
            tokenID.save()
            mail_subject= 'Account Activation' #Email to be sent preparation process
            message= render_to_string('auth/mail/accountActivation.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token
            })
            email= EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(request, 'Please check your email to complete the registration..') #Notifying user after the mail has been sent
            return redirect('index')
    return render(request, 'auth/register.html', context= {
        'form': RegistrationForm,
        'messages': messages_to_display
    })

# Account activation
def activate(request, uidb64, token): 
    user= auth.get_user_model()

    try: # Decoding the hashes recieved from the link to verify if it a valid link to activate their account
        uid= force_str(urlsafe_base64_decode(uidb64))
        user= User.objects.get(pk= uid)
    except (TypeError, ValidationError, OverflowError, User.DoesNotExist):
        user= None

    if user is not None and TokenGeneratorValidator.check_token(user, token, settings.ACCOUNT_ACTIVATION_TOKEN_EXPIRY_DURATION): # checking the validity of the token
        user.is_active= True
        user.save()
        TokensModel.objects.get(token= token).delete()
        auth.login(request, user)
        messages.success(request, 'Your account has been activated successfully')
        return redirect(reverse('login'))
    else:
        messages.error(request, 'Your account activation failed the link has been expired')
        return redirect('index')
    
def login_page(request, *args, **kwargs):
    messages_to_display= messages.get_messages(request) #Checking if any message is available to be displayed to the user 
    form= LoginForm()
    if request.method == 'POST':
        form= LoginForm(request, data=request.POST)

        if form.is_valid():
            username= form.cleaned_data.get('username')
            password= form.cleaned_data.get('password')
            user= auth.authenticate(request, username= username, password= password)
            if user is not None:
                auth.login(request, user)
            try:
                # userAccount= AccountModel.objects.get(user=request.user)
                if request.user.is_premium:
                    messages.info(request, f'Dear {request.user.username} you have 4 unread notifications.')
            except AccountModel.DoesNotExist:
                messages.info(request, f'Dear {request.user.username} your account is not a premium account you can upgrade to a premium account to enjoy the full benefits.')
                messages.info(request, f'Dear {request.user.username} you have 4 unread notifications.')
            return redirect('index')
        else:
            messages.error(request, f'Make sure your account is veryfied and the credentials are valid')
            return redirect('login')
    else:
        return render(request, 'auth/login.html', context= {
    'form': LoginForm,
    'messages': messages_to_display
    })

def logout_page(request, *args, **kwargs):
    auth.logout(request)
    messages.success(request, ('You have been logged out...'))
    return redirect('index')

def passwordReset(request):
    messages_to_display= messages.get_messages(request)
    form= PasswordResetRequestForm()
    if request.method == 'POST':
        form= PasswordResetRequestForm(request.POST)
        if form.is_valid():
            data= form.cleaned_data.get('email')
            try:
                user= User.objects.get(email= data)
            except (TypeError, ValidationError, User.DoesNotExist):
                user= None

            if user is not None:
                token= TokenGeneratorValidator.make_token(user) #Generating hash 
                tokenID= TokensModel.objects.create(token=token, user_id=user.id) # Registering token to database
                current_site= get_current_site(request) #Geting the curent site domain
                mail_subject= 'Password Reset' #Email to be sent preparation process
                message= render_to_string('auth/mail/passwordResetMail.html', {
                    'user': user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': token
                })
                to_email= form.cleaned_data.get('email')
                email= EmailMessage(
                mail_subject, message, to=[to_email]
            )
                email.send()
                tokenID.save()
                messages.success(request, 'Please check your email to reset your password..')
                return redirect('index')
            
            
            else:
                messages.error(request, 'No account was found with the provided E-mail. Please check and try again...')
                return redirect('password-reset-request')
    return render(request, 'auth/passwordReset.html', context={
        'form': PasswordResetRequestForm,
        'messages': messages_to_display
    })

def passwordResetConfirm(request, uidb64, token):
    user= auth.get_user_model()

    try: # Decoding the hashes recieved from the link to verify if it a valid link to activate their account
        uid= force_str(urlsafe_base64_decode(uidb64))
        user= User.objects.get(pk= uid)
    except (TypeError, ValidationError, OverflowError, User.DoesNotExist):
        user= None
    print(token)
    not_expired = TokenGeneratorValidator.check_token(user, token, settings.PASSWORD_RESET_TOKEN_EXPIRY_DURATION)
    if user is not None and not_expired:
        # TokensModel.delete(token= token)
        return redirect('password-change', id=uidb64)
    else:
        messages.error(request, 'Password reset failed the link has been expired')
        return redirect('index')
    
def passwordChange(request, id):
    forms= PasswordChangeForm()
    if request.method == 'POST':
        form= PasswordChangeForm(request.POST)
        if form.is_valid():
            email= form.cleaned_data.get('email')
            passwordOne= form.cleaned_data.get('passwordOne')
            # passwordTwo= form.cleaned_data.get('passwordTwo')
            try: 
                user= User.objects.get(email= email)
            except (TypeError, ValidationError, User.DoesNotExist):
                user= None
            if user is not None and user.id == int(force_str(urlsafe_base64_decode(id))):
                user.set_password(passwordOne)
                user.save()
                TokensModel.objects.get(user_id= user.id).delete()
                current_site= get_current_site(request) #Geting the curent site domain
                mail_subject= 'Password Reset Confirmation' #Email to be sent preparation process
                message= render_to_string('auth/mail/passwordResetDone.html', {
                    'user': user,
                    'domain': current_site,
                })
                to_email= form.cleaned_data.get('email')
                email= EmailMessage(
                mail_subject, message, to=[to_email]
            )
                email.send()
                messages.success(request, 'Your password has been changed successfully')
                return redirect('index')
            else:
                messages.error(request, 'Password reset failed make sure to use the required E-mail and link')
                return redirect('index')
        else:
            messages.error(request, f'{next(iter(form.errors.values()))[0]}')
            return redirect('index')
    else:
        return render(request, 'auth/newPassword.html', {'form': PasswordChangeForm, 'id': id})