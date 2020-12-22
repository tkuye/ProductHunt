from django.db.models.fields import EmailField
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import django.contrib.auth.password_validation as validators
from django.core import exceptions
def signup(request):
    if request.method == 'POST':
        # User has info and wants an account
        
        if request.POST['password1'] == request.POST['password2']:
            user = User(request.POST['username'], request.POST['password1'], request.POST['email'])
            password = request.POST['password1']
            
            try: 
                validators.validate_password(password=password, user=User)
            except exceptions.ValidationError as e:
                errors = list(e.messages)
                for error in errors:
                    print(error)
                return render(request, 'accounts/signup.html', {'errors':errors})
            
            try: 
                validate_email(request.POST['email'])
            except ValidationError:
                return render(request, 'accounts/signup.html', {'erroro':'Please enter a valid email adress.'})
                
            try:
                user = User.objects.get(email=request.POST['email'])
                return render(request, 'accounts/signup.html', {'erroro':'An account with this email already exists.'}) 
            except User.DoesNotExist:
                    pass
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/signup.html', {'erroro':'Username has already been taken.'})
                
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password1'])
                auth.login(request, user)
                return redirect('home')

        else:
            return render(request, 'accounts/signup.html', {'erroro':'Passwords must match'})

    else: #User wants to enter info
        return render(request, 'accounts/signup.html')

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/login.html', {'error':'Please provide the correct password for this account.'})
            except User.DoesNotExist:
                return render(request, 'accounts/login.html', {'error':'There is no user with that username.'})
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')

