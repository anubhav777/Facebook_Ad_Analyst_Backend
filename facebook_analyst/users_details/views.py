from django.shortcuts import render
from rest_framework import viewsets,permissions
from rest_framework.decorators import action,api_view,permission_classes
from rest_framework.parsers import JSONParser
from  .models import Usersearchhistory,Userpages
from .serializers import Userserializer,Userpgseril,Userdisplayseril,Uservalidator
from pages.models import Pagesdetail
from rest_framework.response import Response
from django.contrib.auth.models import User
import json
from rest_framework.response import Response
from datetime import date
from .files import *
# Create your views here.

# @api_view(['POST',])
# def signupform(request):
#     permission_classes=(permissions.AllowAny,)
#     if request.method == 'POST':
#         data={
#                 'username':request.data['username'],
#                 'email':request.data['email'],
#                 'password':request.data['password']
#             }
#         serializer=Userserializer(data=data)
#         if serializer.is_valid():
#                 serializer.save()
#                 return Response({'status': 'User sucessfully registered'})
#         else:
#                 return Response({'status':'sorry a problem encountered'})
        


class signupform(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=Userserializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (permissions.AllowAny,)
        return super(signupform,self).get_permissions()

@api_view(['POST'])
@permission_classes([permissions.AllowAny,])
def signup_user(request):
    em=request.data['email']
    check_user=None
    try:
        check_user=User.objects.filter(email=request.data['email']).first()
    except Exception as e:
        pass
    if check_user == None:
        seril=Userserializer(data=request.data)
        if seril.is_valid():
            seril.save()
            token_genrator(em)
            return Response({'status':'success'})
        else:
            print(seril.errors)
    return Response({'status':'error'})




@api_view(['POST'])
@permission_classes([permissions.AllowAny,])
def email_validator(request):
    email=request.data['token']
    tok=token_decoder(email)
    
    new_user=User.objects.get(email=tok['email'])
    
    print(new_user)
 
    data={
    }
    data["is_staff"]="True"
   
    print(request.data)

    serializers=Uservalidator(new_user,data=data)
    if serializers.is_valid():
        serializers.save()
        return Response({'status':'success'})
    else:
        return Response({'status':'err'})

@api_view(['POST'])
def reset_password(request,id):
    new_user=User.objects.get(id=id)
    data={
        "email":new_user.email,
        "username":new_user.username,
        "password":request.data['password']
    }
    print(new_user.username)
    serializer=Userserializer(new_user,data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({'status':'updated'})
    return Response({'sataus':'error'})
@api_view(['POST','GET','DELETE'])
def user_pages(request,id):
    if request.method == "POST":
        data_checker=None
    
        product_id=request.META['HTTP_PRODUCTID']
        print(product_id)
        userid=request.user.id
        new_page_id=Pagesdetail.objects.get(page_id=product_id)
        prodid=new_page_id.id
        print(new_page_id.id,'hi')
        bla=Userpages.objects.filter(productid=prodid,userid=userid).first()
        print(bla)
        try:
            data_checker=Userpages.objects.filter(productid=prodid,userid=userid).first()
            print(data_checker)
        except Exception as e:
            pass
        if data_checker == None: 
            data={
                'productid':prodid,
                'userid':userid,
                'date':date.today()
            }
            print(data)
            serializers=Userpgseril(data=data)
            if serializers.is_valid():
                serializers.save()
            else:
                print(serializers.errors)
            print(product_id,userid,new_page_id.id)
            return Response({'status':'success'})
        else:
            return Response({'status':'already uploaded'})
    elif request.method == 'GET':
        userid=request.user.id
        queryset=None
        if request.user.is_superuser:
            queryset=Userpages.objects.all()
            ad=admin_pages()
            return Response({'status':ad})
        else:
            queryset=Userpages.objects.filter(userid=userid).all()

        
        serializers=Userdisplayseril(queryset,many=True)
        
        return Response({'status':serializers.data})
    elif request.method == "DELETE":
        serializers=Userpages.objects.get(pk=id)
        serializers.delete()
        return Response({'status':'success'})