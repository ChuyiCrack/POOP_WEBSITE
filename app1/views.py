from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm,Modify_Account_Form
from .models import poop_account,poops,friend_request,profile_comment,group_poop , Group_Notification
from django.utils import timezone
from django.db.models import Q
from django.http import Http404,HttpResponse
from .functions import remove_user_group


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
    user=request.user
    if not user.is_authenticated:
        return redirect('index')
    Account = get_object_or_404(poop_account, owner=request.user)
    
    friends = Account.friends.all()
    
    if 'search' in request.POST:
        search = request.POST['user_input']
        friends = Account.friends.filter(owner__username__contains=search)

    context= {
        'account':Account,
        'friends':friends,
    }
    
    return render(request,'home.html',context)

def profile(request,pk):
    Account=poop_account.objects.get(owner=request.user)
    print(Account.check_notifications())
    profile_ac=poop_account.objects.get(id=pk)
    all_coments = profile_comment.objects.filter(recipent = profile_ac).order_by('-dtae')
    has_sent_fr = True if friend_request.objects.filter(sender = Account , receiver = profile_ac).exists() else False
    if 'submit_comment' in request.POST:
        if request.POST['user_comment']:
                user_coment = request.POST['user_comment']
                if not(len(user_coment) >= 500 ):
                    profile_comment.objects.create(
                        author = Account,
                        recipent = profile_ac,
                        message = user_coment
                    )
        else:
            print("You need to write something to post a comment")

    elif 'delete_comment' in request.POST:
        id_comment = request.POST['delete_comment']
        profile_comment.objects.get(id=id_comment).delete()
        return redirect('profile',profile_ac.id)

    elif 'remove_friend' in request.POST:
        Account.friends.remove(profile_ac)
        Account.save()
        return redirect('profile',profile_ac.id)

    elif 'send_friend_request' in request.POST:
        friend_request.objects.create(type="friend_request" , sender = Account , receiver= profile_ac)
        return redirect('profile',profile_ac.id)
    
    elif 'remove_fr' in request.POST:
        friend_request.objects.filter(sender = Account , receiver = profile_ac).delete()
        return redirect('profile',profile_ac.id)

    context={
        'account':Account,
        'profile':profile_ac,
        'all_coments':all_coments,
        'sent':has_sent_fr

    }
    return render(request,'profile.html',context)

def modify_aacount(request):
    Account=poop_account.objects.get(owner=request.user)
    if request.method=='POST':
        form=Modify_Account_Form(request.POST,request.FILES, instance=Account)
        if form.is_valid():
            form.save()
            return redirect('profile',Account.id)

    else:
        form=Modify_Account_Form(instance=Account)

    context={
        'form':form,
        'account':Account,
    }

    return render(request,'modify_account.html',context)

def ranking(request):
    Account=poop_account.objects.get(owner=request.user)
    all_users=poop_account.objects.filter(poops_count__gt=0).order_by('-poops_count')
    if len(all_users)>=3:
        first=all_users[0]
        second=all_users[1]
        third=all_users[2]

    elif len(all_users)==2:
        first=all_users[0]
        second=all_users[1]
        third=None

    elif len(all_users)==1:
        first=all_users[0]
        second=None
        third=None

    else:
        first=None
        second=None
        third=None
    

    
    context={
        'account':Account,
        'top_users':all_users,
        'first':first,
        'second':second,
        'third':third
        
    }
    return render(request,'ranking.html',context)


def adding_friends(request):
    Account = get_object_or_404(poop_account, owner=request.user)
    context = {
        'account':Account,
        'searched':False
    }
    
    if "search" in request.POST:
        user_search = request.POST['user_input']
        found_accounts = poop_account.objects.filter(
            Q(owner__username__contains=user_search) & ~Q(owner = request.user) & ~Q(owner__in = [friend.owner for friend in Account.friends.all()])
                                                     )
        context['found_accounts'] = found_accounts
        if found_accounts.exists():
            context['searched'] = True

    
    return render(request,"add_friends.html",context)


def Create_Group(request):
    Account = get_object_or_404(poop_account, owner=request.user)
    if Account.joined_group:
        return redirect("home")
    if request.POST:
        group_name = request.POST['group_name']
        if len(group_name) > 0:
            instance = group_poop.objects.create(owner = Account , group_name = group_name)
            instance.members.add(Account)
            instance.save()
            Account.joined_group = instance
            Account.save()
        else:
            pass

    context = {
        'account':Account,
    }
    return render(request,"create_group.html" , context)

def Group_Popp_View(request,pk):
    Account = get_object_or_404(poop_account, owner=request.user)
    print(len(Account.check_gr_sent()))
    try:
        Group = get_object_or_404(group_poop,id=pk)

    except Http404:
        return HttpResponse("<style> body{text-align:center;} </style>"+f"<h2>Group with the id {pk} was not found <br> Try to search with another id</h2> <br> <a href='/'>Go back </a>")
    
    if 'kick_member' in request.POST:
        pk = request.POST['kick_member']
        target_ac = poop_account.objects.get(id = pk)
        remove_user_group(Group,target_ac)
        return redirect("group_poop",Group.id)
    
    if 'invite_member' in request.POST:
        pk = request.POST['invite_member']
        target_ac = poop_account.objects.get(id = pk)
        Group_Notification.objects.create(type = "group" , sender = Account , receiver = target_ac , group = Group)
        return redirect("group_poop",Group.id)

    
    context = {
        'account':Account,
        'group':Group
    }
    return render(request,"poop_group.html" , context)
