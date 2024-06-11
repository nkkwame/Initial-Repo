from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth 
# from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib import messages
from django.urls import reverse
from .tokensGenerator import *
from .forms import *
from .models import *

# Create your views here.
# @login_required(login_url='login')
def index(request):
    messages_to_display= messages.get_messages(request)

    return render(request, 'index.html', context= {
        'messages': messages_to_display
    })

def register_user(request):
    form= RegistrationForm()
    if request.method == 'POST':
        form= RegistrationForm(request.POST)
        if form.is_valid():
            user= form.save(commit= False)
            user.is_active= False
            user.save()
            current_site= get_current_site(request) #Geting the curent site domain
            mail_subject= 'Account Activation' #Email to be sent preparation process
            message= render_to_string('auth/accountActivation.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })
            to_email= form.cleaned_data.get('email')
            email= EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(request, 'Please check your email to complete the registration..') #Notifying user after the mail has been sent
            return redirect('index')
    return render(request, 'auth/register.html', context= {
        'form': RegistrationForm
    })

# Account activation
def activate(request, uidb64, token): 
    user= auth.get_user_model()

    try: # Decoding the hashes recieved from the link to verify if it a valid link to activate their account
        uid= force_str(urlsafe_base64_decode(uidb64))
        user= User.objects.get(pk= uid)
    except (TypeError, ValidationError, OverflowError, User.DoesNotExist):
        user= None

    if user is not None and account_activation_token.check_token(user, token): # checking the validity of the token
        user.is_active= True
        user.save()

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
            return redirect('index')
        else:
            messages.error(request, 'Make sure your account is veryfied and the credentials are valid')
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
    return render(request, 'auth/passwordReset.html')