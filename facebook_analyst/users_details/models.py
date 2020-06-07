from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.utils import timezone
from pages.models import Pagesdetail
# Create your models here.
class Usersearchhistory(models.Model):
    searchquery=models.CharField(max_length=120)
    date=models.DateField(default=timezone.now)
    userid=models.ForeignKey(User,on_delete=models.CASCADE)   

class Userpages(models.Model):
    date=models.DateField(timezone.now)
    productid=models.ForeignKey('pages.Pagesdetail',on_delete=models.CASCADE)
    userid=models.ForeignKey(User,on_delete=models.CASCADE) 