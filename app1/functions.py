from .models import poop_account,group_poop


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
