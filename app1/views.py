from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm,Modify_Account_Form
from .models import poop_account,poops,friend_request,profile_comment,group_poop , Group_Notification, Group_Comment
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from django.http import Http404,HttpResponse
from .functions import remove_user_group, made_poop


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
    
    try:
        Group = get_object_or_404(group_poop,id=pk)

    except Http404:
        return HttpResponse("<style> body{text-align:center;} </style>"+f"<h2>Group with the id {pk} was not found <br> Try to search with another id</h2> <br> <a href='/'>Go back </a>")
    
    all_comments = Group_Comment.objects.filter(group = Group).order_by("-date")
    if 'kick_member' in request.POST:
        pk = request.POST['kick_member']
        target_ac = poop_account.objects.get(id = pk)
        remove_user_group(Group,target_ac)
    
    elif 'invite_member' in request.POST:
        pk = request.POST['invite_member']
        target_ac = poop_account.objects.get(id = pk)
        Group_Notification.objects.create(type = "group" , sender = Account , receiver = target_ac , group = Group)
    
    elif 'post_comment' in request.POST and len(request.POST['chat_input']) > 0:
        text = request.POST['chat_input']
        if len(text) <= 500:
            Group_Comment.objects.create(author = Account , group = Group , message = text)
    
    elif 'remove-comment' in request.POST:
        comment_id = request.POST['remove-comment']
        Group_Comment.objects.get(id=comment_id).delete()
    
    elif 'made_poop' in request.POST:
        poops.objects.create(owner_shit = Account)
        made_poop(Account)
    
    if request.method == "POST":
        return redirect("group_poop",Group.id)
    
    all_players = Group.players_ordered()
    ordered_players = [None , None , None]
    for i in range(len(all_players)):
        if i > 3:
            break
        ordered_players[i] = all_players[i]
    
    two_hours_ago = timezone.now() - timedelta(hours=2)
    last_poop = poops.objects.filter(owner_shit = Account ,date__gt=two_hours_ago)
    if last_poop.exists():
        can_button= False
        last_poop_time = last_poop[0].date

    else:
        can_button = True
        last_poop_time= None
    
    context = {
        'account':Account,
        'group':Group,
        'comments':all_comments,
        'first_place':ordered_players[0],'second_place':ordered_players[1],'third_place':ordered_players[2],
        'can_button':can_button,
        'last_poop_time':last_poop_time
    }
    return render(request,"poop_group.html" , context)
