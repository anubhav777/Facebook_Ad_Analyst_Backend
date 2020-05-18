from django.shortcuts import render
from rest_framework import viewsets,permissions
from rest_framework.decorators import action,api_view
from  .models import Usersearchhistory
from .serializers import Userserializer,UserSearchdisp
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


