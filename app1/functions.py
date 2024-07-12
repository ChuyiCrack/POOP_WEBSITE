from .models import poop_account,group_poop,Notification,Group_Notification,friend_request
from django.shortcuts import render,redirect,get_object_or_404


def add_to_group(target_user:poop_account ,target_group:group_poop):
    if not target_user.group:
        target_user.group = target_group
        target_group.members.add(target_user)
        target_user.save()
        target_group.save()

    else:
        return "The user already has a group"

def remove_user_group(target_group:group_poop,target_user:poop_account):
    target_group.members.remove(target_user)
    target_group.save()
    target_user.joined_group = None
    target_user.save()
    return


def Requests_Navbar(request):
    Account = get_object_or_404(poop_account, owner=request.user)
    if 'join_group' in request.POST:
        id = request.POST['join_group']
        instance = Group_Notification.objects.get(id=id)
        instance.group.members.add(Account)
        Account.joined_group = instance.group
        instance.group.save()
        Account.save()
        instance.delete()
        

    elif 'deny_group' in request.POST:
        id = request.POST['delete']
        instance = Group_Notification.objects.get(id=id)
        instance.delete()

    elif 'accept_friend' in request.POST:
        id = request.POST['accept_friend']
        instance = friend_request.objects.get(id=id)
        Account.friends.add(instance.sender)
        Account.save()
        instance.delete()

    elif 'deny_friend' in request.POST:
        id = request.POST['deny_friend']
        instance = friend_request.objects.get(id=id)
        instance.delete()
    
    return redirect('home')
