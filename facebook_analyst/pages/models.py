from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone
# Create your models here.
class Pagesdetail(models.Model):
    page_id=models.CharField(max_length=128,null=False,unique=True)
    page_name=models.CharField(max_length=128,null=False)
    socialmedia=JSONField()
    page_info=JSONField()
    searched_date=models.DateField(default=timezone.now,blank=True)
    total_ads=models.CharField(max_length=128,blank=True)
    insatgram_tracker=JSONField(blank=True,default=dict)
    facebook_tracker=JSONField(blank=True,default=dict)

class Addetails(models.Model):
    adid=models.CharField(max_length=128,null=False)
    start_date=models.CharField(max_length=128,blank=True)
    end_date=models.CharField(max_length=128,blank=True)
    created_time=models.CharField(max_length=128,blank=True)
    searched_date=models.DateField(default=timezone.now)
    ad_info=JSONField()
    mul_type=models.CharField(max_length=128,blank=True)
    mul_type_link=models.CharField(max_length=5000,blank=True)
    productid=models.ForeignKey('Pagesdetail',on_delete=models.CASCADE)
    userid=models.ForeignKey(User,on_delete=models.CASCADE)

class Expiredads(models.Model):
    searched_date=models.DateField(default=timezone.now)
    adsid=models.ForeignKey('Addetails',on_delete=models.CASCADE)
    productid=models.ForeignKey('Pagesdetail',on_delete=models.CASCADE)

class Socialmedia_tracker(models.Model):
    fb_likes=models.CharField(max_length=128)
    insta_likes=models.CharField(max_length=128)
    fb_stats=models.CharField(max_length=128,blank=True)
    insta_stats=models.CharField(max_length=128,blank=True)
    date=models.DateField(default=timezone.now)
    productid=models.ForeignKey('Pagesdetail',on_delete=models.CASCADE)

class Adstracker(models.Model):
    year=models.CharField(max_length=128)
    month=models.CharField(max_length=128)
    date=models.CharField(max_length=128)
    weekday=models.CharField(max_length=128)
    adid=models.ForeignKey('Addetails',on_delete=models.CASCADE)