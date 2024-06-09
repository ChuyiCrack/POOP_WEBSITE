from typing import Iterable
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils import timezone

class poops(models.Model):
    date=models.DateTimeField(default=timezone.now)
    owner_shit=models.ForeignKey(User,on_delete=models.CASCADE,default=None)

    def __str__(self):
        return self.owner_shit.username


class poop_account(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    profile_img=models.ImageField(upload_to='./images',blank=True,default='./used_media/default.jpg')
    description=models.TextField(max_length=150,blank=True)
    poops_count=models.IntegerField(default=0)
    friends = models.ManyToManyField('self',symmetrical=True,blank=True)
    joined_group = models.ForeignKey("group_poop" ,blank=True, null=True , default=None ,on_delete=models.DO_NOTHING)
    comments = models.ManyToOneRel

    def __str__(self):
        return self.owner.username
    

class group_poop (models.Model):
    owner_group = models.ForeignKey(User,on_delete=models.CASCADE)
    name_group = models.CharField(max_length=35 , blank=False)
    players_joined = models.PositiveIntegerField(default=1)


    def __str__(self) -> str:
        return self.name_group
    
class friend_request(models.Model):
    sender = models.ForeignKey(poop_account,on_delete=models.CASCADE , related_name="sender_request")
    receiver = models.ForeignKey(poop_account,on_delete=models.CASCADE,related_name="receiver_request")
    date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        
        if friend_request.objects.filter(sender = self.sender , receiver = self.receiver).exists():
            friend_request.objects.filter(sender = self.sender , receiver = self.receiver).delete()

        # Call the original save method
        super().save(*args, **kwargs)


    def __str__(self) -> str:
        return f"From {self.sender} to {self.receiver} at {self.date}"
    

class profile_comment(models.Model):
    author = models.ForeignKey(poop_account ,on_delete=models.CASCADE , related_name='sender')
    recipent = models.ForeignKey(poop_account,on_delete=models.CASCADE , related_name='recipent_user')
    message = models.TextField(max_length=1000 , blank=False)
    dtae = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"Message from {self.author} to {self.recipent}"
