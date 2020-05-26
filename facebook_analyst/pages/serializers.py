from rest_framework import serializers
from .models import Pagesdetail,Addetails,Expiredads

class Pagesseril(serializers.ModelSerializer):
    class Meta:
        model=Pagesdetail
        fields=('id','page_id','page_name','socialmedia','page_info','facebook_tracker','insatgram_tracker')

class Adserial(serializers.ModelSerializer):
    class Meta:
        model=Addetails
        fields=('id','adid','start_date','end_date','searched_date','ad_info','productid','userid','created_time')
class Expireserial(serializers.ModelSerializer):
    adsid=Adserial(read_only=True)
    class Meta:
        model=Expiredads
        fields=('id','searched_date','productid','adsid')