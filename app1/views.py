from django.shortcuts import render,redirect
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm,Modify_Account_Form
from .models import poop_account


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
            account=poop_account(owner=user)
            account.save()
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
    Account=poop_account.objects.get(owner=request.user)
    context={
        'account':Account
    }
    return render(request,'home.html',context)

def profile(request):
    Account=poop_account.objects.get(owner=request.user)
    context={
        'account':Account
    }
    return render(request,'profile.html',context)

def modify_aacount(request):
    Account=poop_account.objects.get(owner=request.user)
    if request.method=='POST':
        form=Modify_Account_Form(request.POST,request.FILES, instance=Account)
        if form.is_valid():
            form.save()
            return redirect('profile')

    else:
        form=Modify_Account_Form(instance=Account)

    context={
        'form':form
    }

    return render(request,'modify_account.html',context)
