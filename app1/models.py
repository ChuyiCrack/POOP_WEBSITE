from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class poops(models.Model):
    date=models.DateTimeField(default=timezone.now)
    owner_shit=models.ForeignKey(User,on_delete=models.CASCADE,default=None)

    def __str__(self):
        return self.owner_shit.username


class poop_account(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    profile_img=models.ImageField(upload_to='./images',blank=True,default='./images/default.jpg')
    description=models.TextField(max_length=150,blank=True)
    poops_count=models.IntegerField(default=0)

    def __str__(self):
        return self.owner.username
