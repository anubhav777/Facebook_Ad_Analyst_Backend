from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from datetime import date
# Create your models here.
class Pagesdetail(models.Model):
    page_id=models.CharField(max_length=128,null=False,unique=True)
    page_name=models.CharField(max_length=128,null=False)
    socialmedia=JSONField()
    page_info=JSONField()

class Addetails(models.Model):
    adid=models.CharField(max_length=128,null=False)
    start_date=models.CharField(max_length=128,blank=True)
    end_date=models.CharField(max_length=128,blank=True)
    searched_date=models.DateField(default=date.today())
    ad_info=JSONField()
    productid=models.ForeignKey('Pagesdetail',on_delete=models.CASCADE)
    userid=models.ForeignKey(User,on_delete=models.CASCADE)

    