from rest_framework import serializers
from .models import Pagesdetail,Addetails,Expiredads,Socialmedia_tracker,Adstracker

class Pagesseril(serializers.ModelSerializer):
    class Meta:
        model=Pagesdetail
        fields=('id','page_id','page_name','socialmedia','searched_date','page_info','total_ads','facebook_tracker','insatgram_tracker')

class Adserial(serializers.ModelSerializer):
   
    class Meta:
        model=Addetails
        fields=('id','adid','start_date','end_date','searched_date','ad_info','productid','userid','created_time','mul_type','mul_type_link')
    def to_representation(self,instance):
        self.fields['productid']=Pagesseril(read_only=True)
        return super(Adserial,self).to_representation(instance)
class Expireserial(serializers.ModelSerializer):
    adsid=Adserial(read_only=True)
    class Meta:
        model=Expiredads
        fields=('id','searched_date','productid','adsid')
class Socialmedia_seril(serializers.ModelSerializer):
    class Meta:
        model=Socialmedia_tracker
        fields=('id','fb_likes','insta_likes','fb_stats','insta_stats','date','productid')

class Adsseril(serializers.ModelSerializer):
    
    class Meta:
        model=Adstracker
        fields=('id','year','month','date','weekday','adid')
    def to_representation(self, instance):
        self.fields['adid'] =  Adserial(read_only=True)
        return super(Adsseril, self).to_representation(instance)