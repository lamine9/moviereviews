from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from accounts.forms import UserCreateForm

# Create your views here.
def signupaccount(request):
    if request.method == 'GET':
        return render(request, 'signupaccount.html', {'form': UserCreateForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                print(user.password)
                user.save()
                # user = authenticate(request, username=request.POST['username'], password=request.POST['password1'])
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signupaccount.html', {'form': UserCreateForm, 'error': 'Username already taken. Choose new username.'})
        else:
            return render(request, 'signupaccount.html', {'form': UserCreateForm, 'error': 'Passwords do not match.'})

@login_required 
def logoutaccount(request):
    logout(request)
    return redirect('home')

def loginaccount(request):
    if request.method == 'GET':
        return render(request, 'loginaccount.html', {'form': AuthenticationForm})
    else:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'loginaccount.html', {'form': AuthenticationForm(),'error': 'Username and password do not match'})
        else:
            login(request, user)
            return redirect('home')