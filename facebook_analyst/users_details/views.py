from django.shortcuts import render
from rest_framework import viewsets,permissions
from rest_framework.decorators import action,api_view
from rest_framework.parsers import JSONParser
from  .models import Usersearchhistory
from .serializers import Userserializer,UserSearchdisp,Uservalidator
from rest_framework.response import Response
from django.contrib.auth.models import User
import json
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

    # @action(detail=False,methods=['get','delete'])
    # def newuser(self,request,**kwargs):
    #     queryset=User.objects.all()
    #     serializer_class=Userserializer
    #     permission_classes=(permissions.IsAuthenticated)
    #     result={'hi':'hi'}
    #     return Response({'status':result})
       
    #     # print('hi')
    #     # if request.method == "POST":
    #     #     data={
    #     #         'username':request.data['username'],
    #     #         'email':request.data['email'],
    #     #         'password':request.data['password']
    #     #     }
    #     #     serializer=Userserializer(data=data)
    #     #     if serializer.is_valid():
    #     #         serializer.save()
    #     #         return Response({'status': 'User sucessfully registered'})
    #     #     else:
    #     #         return Response({'status':'sorry a problem encountered'})
        



class displaysearch(viewsets.ModelViewSet):
    queryset=Usersearchhistory.objects.all()
    serializer_class=UserSearchdisp


@api_view(['POST'])
def email_validator(request,email):
    new_user=User.objects.get(email=email)
    print(new_user)
    # data={
    # }
    # data["is_staff"]="True"
   
    print(request.data)

    serializers=Uservalidator(new_user,data=request.data)
    if serializers.is_valid():
        serializers.save()
        return Response({'status':'hi'})
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
