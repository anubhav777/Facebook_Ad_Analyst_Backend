from django.db import models
from datetime import date
from django.contrib.auth.models import User
# Create your models here.
class Usersearchhistory(models.Model):
    searchquery=models.CharField(max_length=120)
    date=models.DateField(default=date.today())
    userid=models.ForeignKey(User,on_delete=models.CASCADE)   
