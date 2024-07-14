from django.contrib import admin
from .models import poop_account,poops,friend_request,profile_comment,group_poop,Group_Notification,Notification,Group_Comment


admin.site.register(poop_account)
admin.site.register(poops)
admin.site.register(friend_request)
admin.site.register(profile_comment)
admin.site.register(group_poop)
admin.site.register(Notification)
admin.site.register(Group_Notification)
admin.site.register(Group_Comment)
