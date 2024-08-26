from .models import poop_account,group_poop,Notification,Group_Notification,friend_request,Group_Comment
from django.shortcuts import render,redirect,get_object_or_404


def add_to_group(target_user:poop_account ,target_group:group_poop):
    if not target_user.joined_group:
        target_user.joined_group = target_group
        target_group.members.add(target_user)
        Group_Comment.objects.create(
            group = target_group ,
            message = f"{target_user} joined the group",
            type_message = "global",
            )
        target_user.save()
        target_group.save()

    else:
        return "The user already has a group"

def remove_user_group(target_group:group_poop,target_user:poop_account,kicked_by:poop_account=None):
    target_group.members.remove(target_user)
    target_group.save()
    target_user.joined_group = None
    target_user.group_poops = 0
    target_user.save()
    message = f"{target_user} was kicked by {kicked_by}" if kicked_by else f"{target_user} left the group"
    Group_Comment.objects.create(
            group = target_group ,
            message = message,
            type_message = "global",
            )
    return


def Requests_Navbar(request):
    Account = get_object_or_404(poop_account, owner=request.user)
    if 'join_group' in request.POST:
        id = request.POST['join_group']
        instance = Group_Notification.objects.get(id=id)
        add_to_group(Account ,instance.group)
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


def made_poop(target_user:poop_account):
    target_user.global_poops+=1
    target_user.group_poops+=1
    target_user.save()
    return
