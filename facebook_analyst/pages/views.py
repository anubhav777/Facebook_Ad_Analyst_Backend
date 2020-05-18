from django.shortcuts import render
from django.core import serializers
from rest_framework import viewsets,status,permissions
from .models import Pagesdetail,Addetails
from.serializers import Pagesseril,Adserial
from rest_framework.decorators import action,api_view,permission_classes
from rest_framework.response import Response
from django.http import HttpResponse
from datetime import date
from .files import *
# Create your views here.
class Displaypages(viewsets.ModelViewSet):
    queryset=Pagesdetail.objects.all()
    serializer_class=Pagesseril

@api_view(['POST','PUT','DELETE'])
def insert_pages(request,id=None):
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
            serializers=Pagesseril(filter_data,data=prod_func)
        if serializers.is_valid():
                serializers.save()
                return Response({'status':'added'})
        else:
                return Response({'status':'error'})
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
        all_data=facebook_ad_details(token,userid.id,id,country_filter,days,platform)
        return Response({'status':all_data})
