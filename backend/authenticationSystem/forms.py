from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegistrationForm(UserCreationForm):
    email= forms.EmailField(required= True)
    firstName= forms.CharField(required= True)
    lastName= forms.CharField(required= True)
    
    class Meta:
        model= User
        fields= ['firstName', 'lastName', 'username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    # username= forms.CharField(required= True)

    class Meta:
        fields= ['username', 'password']
    

    def clean_email(self):
        email= self.cleaned_data.get('email')
        if User.objects.filter(email= email).exists():
            raise ValidationError('An account with this email address already exists')
        return email