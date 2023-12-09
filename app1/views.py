from django.shortcuts import render,redirect
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm


def index(request):
    user=request.user
    if request.method == 'POST':
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect('home')
        
    elif user.is_authenticated:
        return redirect('home')

    else:
        form=AuthenticationForm()
    context = {
        'form':form,
    }
    return render(request,'index.html',context)


def register(request):
    if request.method == 'POST':
        form=CustomUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('index')

    else:
        form=CustomUserCreationForm()
    context = {
        'form':form,
    }
    return render(request,'register.html',context)

def logout_user(request):
    logout(request)
    return redirect('index')

def home(request):
    return render(request,'home.html')
