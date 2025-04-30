from typing import Iterable
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils import timezone
from django.db.models import Value,CharField

class poops(models.Model):
    date=models.DateTimeField(default=timezone.now)
    owner_shit=models.ForeignKey("poop_account",on_delete=models.CASCADE,default=None)

    def __str__(self):
        return f"{self.owner_shit.owner.username} at {self.date}"


class poop_account(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    profile_img=models.ImageField(upload_to='./images',blank=True,default='./used_media/default.jpg')
    description=models.TextField(max_length=150,blank=True)
    global_poops=models.PositiveIntegerField(default=0)
    group_poops = models.PositiveIntegerField(default=0)
    friends = models.ManyToManyField('self',symmetrical=True,blank=True)
    joined_group = models.ForeignKey("group_poop" ,blank=True, null=True , default=None ,on_delete=models.SET_NULL , related_name='poop_accounts')
    comments = models.ManyToOneRel

    def check_gr_sent(self):
        return [gr.receiver for gr in Group_Notification.objects.filter(sender = self).all()]
    
    def check_notifications(self):
        noti_group = Group_Notification.objects.filter(receiver = self)
        noti_friend = friend_request.objects.filter(receiver = self)
        noti_friend = noti_friend.annotate(extra=Value(None,output_field=CharField()))
        
        return noti_group.union(noti_friend).order_by('-date').all()

    def __str__(self):
        return self.owner.username

class profile_comment(models.Model):
    author = models.ForeignKey(poop_account ,on_delete=models.CASCADE , related_name='sender')
    recipent = models.ForeignKey(poop_account,on_delete=models.CASCADE , related_name='recipent_user')
    message = models.TextField(max_length=1000 , blank=False)
    dtae = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"Message from {self.author} to {self.recipent}"
    
class Group_Comment(models.Model):
    author = models.ForeignKey(poop_account ,on_delete=models.CASCADE ,blank=True,null=True,  related_name='authro_gc')
    group = models.ForeignKey("group_poop" ,blank=True, null=True , default=None ,on_delete=models.CASCADE)
    message = models.TextField(max_length=500 , blank=False)
    type_message = models.CharField(max_length=30, default="chat")
    date = models.DateTimeField(default=timezone.now)

class group_poop(models.Model):
    owner = models.ForeignKey(poop_account , on_delete=models.CASCADE , blank=False , related_name="owner_group")
    group_name = models.CharField(max_length=50 , unique=True)

    def allMembers(self):
        return self.poop_accounts.all()

    def num_members(self):
        return self.allMembers().count()

    def players_ordered(self):
        players = [member for member in self.allMembers() if member.group_poops > 0]
        return sorted(players , key= lambda x:x.global_poops, reverse=True)

    def __str__(self) -> str:
        return f"{self.group_name}({self.num_members()} members)"
    

class Notification(models.Model):
    type = models.CharField(max_length=25, blank=False, null=False)
    sender = models.ForeignKey(poop_account,on_delete=models.CASCADE,related_name="receiver_notification")
    receiver= models.ForeignKey(poop_account,on_delete=models.CASCADE,related_name="sender_notification")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.type} ---> from {self.sender} to {self.receiver} {self.id}"

class Group_Notification(Notification):
    group = models.ForeignKey("group_poop",on_delete=models.CASCADE,related_name="group_notification")



class friend_request(Notification):
    def save(self, *args, **kwargs):
        if friend_request.objects.filter(sender = self.sender , receiver = self.receiver).exists():
            friend_request.objects.filter(sender = self.sender , receiver = self.receiver).delete()

        # Call the original save method
        if friend_request.objects.filter(sender =self.receiver, receiver = self.sender).exists():
            friend_request.objects.filter(sender =self.receiver, receiver = self.sender).delete()
            self.receiver.friends.add(self.sender)
            self.receiver.save()
            return
        
        super().save(*args, **kwargs)



    