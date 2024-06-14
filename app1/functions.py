from .models import poop_account,poop_group


def add_to_group(target_user:poop_account ,target_group:poop_group):
    if not target_user.group:
        target_user.group = target_group
        target_group.members.add(target_user)
        target_user.save()
        target_group.save()

    else:
        return "The user already has a group"
