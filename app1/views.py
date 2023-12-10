from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm,Modify_Account_Form
from .models import poop_account,poops
from django.utils import timezone

def Count_Poops(user):
    all_poops=poops.objects.all()
    count=0
    for x in all_poops:
        if x.owner_shit==user.owner:
            count+=1
    return count



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
    Account = get_object_or_404(poop_account, owner=request.user)
    time_now=timezone.now()
    All_Poops= poops.objects.filter(owner_shit=Account.owner).order_by('-date')
    if len(All_Poops)>0:
        last_poop=All_Poops[0].date
        diference=time_now-last_poop
        if diference.total_seconds() > 7200:
            can=True

        else:
            can=False

    else:
        can=True
            
    if request.method=='POST':
        user_poop=poops.objects.create(owner_shit=Account.owner)
        Account.poops_count+=1
        Account.save()
        return redirect('home')

    total_poops=Count_Poops(Account)
    context={
        'account':Account,
        'count':total_poops,
        'can':can
    }
    return render(request,'home.html',context)

def profile(request):
    Account=poop_account.objects.get(owner=request.user)
    count=Count_Poops(Account)
    context={
        'account':Account,
        'count':count
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
