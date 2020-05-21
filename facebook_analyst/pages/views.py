from django.shortcuts import render
from django.core import serializers
from rest_framework import viewsets,status,permissions
from .models import Pagesdetail,Addetails
from.serializers import Pagesseril,Adserial
from rest_framework.decorators import action,api_view,permission_classes
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.http import HttpResponse
from datetime import date
from .files import *

# Create your views here.
class Displaypages(viewsets.ModelViewSet):
    queryset=Pagesdetail.objects.all()
    serializer_class=Pagesseril

@api_view(['POST','PUT','DELETE','GET'])
def insert_pages(request,id=None):
    new_user=request.user
    if request.method == "POST":
        product_id=request.META['HTTP_PRODUCTID']
        country=request.META['HTTP_COUNTRY']
        prod_func=facebook_ad_owner(product_id,country)
        filter_data=None
        try:  
            filter_data=Pagesdetail.objects.get(page_id=product_id)
        except Exception as e:
            pass
        serializers=None
        if not filter_data or filter_data == None:
            serializers=Pagesseril(data=prod_func)
        else:
            old_date=None
            new_date=date.today()
            updated_date=new_date.strftime('%d-%m-%Y')
            instagram_data=None
            facebook_data=None
            try:
                old_date=filter_data.facebook_tracker['updated_date']
            except Exception as e:
                pass
            if old_date == None or old_date != updated_date:
                data=None
                old_instagram_followers=filter_data.socialmedia['instagram_followers']
                new_instagram_followers=prod_func['socialmedia']['instagram_followers'] - filter_data.socialmedia['instagram_followers']
                instagram_status=None
                old_facebook_like=filter_data.socialmedia['facebook_like']
                new_facebook_like=prod_func['socialmedia']['facebook_like'] - filter_data.socialmedia['facebook_like']
                facebook_status=None
                if new_instagram_followers > 0:
                    instagram_status='Increment'
                else:
                    instagram_status='Decrement'
                if new_facebook_like > 0:
                    facebook_status='Increment'
                else:
                    facebook_status='Decrement'
                
                instagram_data={'new_followers':new_instagram_followers,'instagram_status':instagram_status,'updated_date':updated_date}
                facebook_data={'new_likes':new_facebook_like,'facebook_status':facebook_status,'updated_date':updated_date}
                
                
                print(old_date)
            else:
                instagram_data=filter_data.insatgram_tracker
                facebook_data=filter_data.facebook_tracker
               
            instagram={'insatgram_tracker':instagram_data}
            facebook={'facebook_tracker':facebook_data}
            prod_func.update(facebook)
            prod_func.update(instagram)
                
            print(prod_func)
            
            serializers=Pagesseril(filter_data,data=prod_func)
            if serializers.is_valid():
                    serializers.save()
                    return Response({'status':'added'})
            else:
                    return Response({'status':'error'})
    elif request.method == 'GET':
        serializer = None
        if not new_user.is_superuser:
            queryobj=Pagesdetail.objects.filter(userid=new_user.id).all()
            serializer=Pagesseril(queryobj,many=True)
        else:
            queryobj=Pagesdetail.objects.all()
            serializer=Pagesseril(queryobj,many=True)
        return Response({'stats':serializer.data})
        


    elif request.method == "DELETE":
        serializers=Pagesdetail.objects.get(pk=id)
        serializers.delete()
        return  Response({'status':'deleted'})

@api_view(['GET','POST'])
def modified_get(request):
    if request.method == "GET":
        queryobj=None
        new_user=request.user
        serializer=None
        print(new_user.is_superuser,new_user.id)
        if(new_user.is_superuser):
            queryobj=Addetails.objects.all()
            serializer=Adserial(queryobj,many=True)
        else:
            queryobj=Addetails.objects.filter(userid=new_user.id).all()
            serializer=Adserial(queryobj,many=True)
            print(request.META['HTTP_AUTHORIZATION'])
        return Response(serializer.data)
    if request.method == "POST":
            data_filter=Addetails.objects.filter(adid=request.data['adid'])
            print(request.data)
            if not data_filter:
                serializer=Adserial(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'status': 'Data sucessfully added'})
                else:
                    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'stats':'already added'})
           

@api_view(['POST'])
def ad_data(request):
    if request.method == 'POST':
        id=request.META['HTTP_PRODUCTID']
        country_filter=request.META['HTTP_FILTER']
        days=request.META['HTTP_DAYS']
        platform=None
        token=request.META['HTTP_AUTHORIZATION']
        userid=request.user
        print(userid.id)
        if request.META['HTTP_PLATFORM'] == "False":
            platform=False
        else:
            platform=request.META['HTTP_PLATFORM']
        # all_data=facebook_ad_details(token,userid.id,id,country_filter,days,platform)
        # return Response({'status':all_data})
        mail=token_genrator('genjilama007@gmail.com')
        return Response({'stats':mail})

