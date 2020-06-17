from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from .models import Usersearchhistory,Userpages
from pages.serializers import Pagesseril
from pages.models import Pagesdetail
class Userserializer(serializers.ModelSerializer):
    email=serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    username=serializers.CharField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    password=serializers.CharField(min_length=8)

    def create(self,validated_data):
        user= User.objects.create_user(validated_data['username'],validated_data['email'],validated_data['password'])
        return user
    
    class Meta:
        model=User
        fields=('id','email','username','password')
        extra_kwargs={
            'password':{'write_only':True}
        }
# class Newprod(serializers.ModelSerializer):
#     class Meta:
#         model=Pa
class Userpgseril(serializers.ModelSerializer):
  
    class Meta:
        model=Userpages
        fields=('id','date','productid','userid')
class Userdisplayseril(serializers.ModelSerializer):
    productid=Pagesseril(read_only=True)
    class Meta:
        model=Userpages
        fields=('id','date','productid','userid')
    def to_representation(self,instance):
        self.fields['productid']=Pagesseril(read_only=True)
        return super(Userdisplayseril,self).to_representation(instance)

class Uservalidator(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['is_staff']
# class UserSearchdisp(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model=Usersearchhistory
#         fields=('id','searchquery','userid','date')

