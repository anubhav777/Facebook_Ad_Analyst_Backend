from django.shortcuts import render
from django.core import serializers
from rest_framework import viewsets,status,permissions
from .models import Pagesdetail,Addetails,Expiredads,Socialmedia_tracker,Adstracker
from.serializers import Pagesseril,Adserial,Expireserial,Socialmedia_seril,Adsseril
from rest_framework.decorators import action,api_view,permission_classes
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.http import HttpResponse
from datetime import date
from datetime import datetime,date
from .files import *
from rest_framework.parsers import JSONParser
import pycountry

# Create your views here.
import json
class Displaypages(viewsets.ModelViewSet):
    queryset=Pagesdetail.objects.all()
    serializer_class=Pagesseril

@api_view(['POST','PUT','DELETE','GET'])
def insert_pages(request,id=None):
    new_user=request.user
   
    if request.method == "POST":
        new_user=request.user
        product_id=request.META['HTTP_PRODUCTID']
        country=request.META['HTTP_COUNTRY']
        new_func=page_getter(product_id,country,new_user.id)
       
        return Response({'stats':new_func})
        
        # call_func=country_getter(product_id)
      
        # filter_data=None
        # try:  
        #     filter_data=Pagesdetail.objects.get(page_id=product_id)
        # except Exception as e:
        #     pass
        # serializers=None
        # if not filter_data or filter_data == None:
        #     prod_func=facebook_ad_owner(product_id,country,new_user.id)
        #     serializers=Pagesseril(data=prod_func)
        #     if serializers.is_valid():
        #         serializers.save()
        #     else:
        #         print(serializers.errors)
        #     return Response({'status':serializers.data,'countries':call_func})
        # else:
        #     prod_func=facebook_ad_owner(product_id,country)
        #     old_date=None
        #     new_date=date.today()
        #     updated_date=new_date.strftime('%d-%m-%Y')
        #     instagram_data=None
        #     facebook_data=None
        #     try:
        #         old_date=filter_data.facebook_tracker['updated_date']
        #     except Exception as e:
        #         pass
        #     if old_date == None or old_date != updated_date:
        #         data=None
        #         old_instagram_followers=filter_data.socialmedia['instagram_followers']
        #         new_instagram_followers=None
        #         if old_instagram_followers == None:
        #             new_instagram_followers="No Connected Instagram Page"
        #         else:
        #             new_instagram_followers=prod_func['socialmedia']['instagram_followers'] - filter_data.socialmedia['instagram_followers']
        #         instagram_status=None
        #         old_facebook_like=filter_data.socialmedia['facebook_like']
        #         new_facebook_like=prod_func['socialmedia']['facebook_like'] - filter_data.socialmedia['facebook_like']
        #         facebook_status=None
        #         if new_instagram_followers == "No Connected Instagram Page":
        #             instagram_status="No Instagramm data"
        #         else:
        #             if new_instagram_followers > 0:
        #                 instagram_status='Increment'
        #             else:
        #                 instagram_status='Decrement'
        #         if new_facebook_like > 0:
        #             facebook_status='Increment'
        #         else:
        #             facebook_status='Decrement'
                
        #         instagram_data={'new_followers':new_instagram_followers,'instagram_status':instagram_status,'updated_date':updated_date}
        #         facebook_data={'new_likes':new_facebook_like,'facebook_status':facebook_status,'updated_date':updated_date}
                
        #         data={
        #             'fb_likes':prod_func['socialmedia']['facebook_like'],
        #             'insta_likes':prod_func['socialmedia']['instagram_followers'],
        #             'fb_stats':new_facebook_like,
        #             'insta_stats':new_instagram_followers,
        #             'date':date.today(),
        #             'productid':filter_data.id
        #         }
        #         print(filter_data.id,'hi')
        #         track_seril=Socialmedia_seril(data=data)
        #         if track_seril.is_valid():
        #             track_seril.save()
        #         else:
        #             print(track_seril.errors)
        #         print(old_date)
        #     else:
        #         instagram_data=filter_data.insatgram_tracker
        #         facebook_data=filter_data.facebook_tracker
               
        #     instagram={'insatgram_tracker':instagram_data}
        #     facebook={'facebook_tracker':facebook_data}
        #     prod_func.update(facebook)
        #     prod_func.update(instagram)
           
            
        #     serializers=Pagesseril(filter_data,data=prod_func)
        #     if serializers.is_valid():
        #             serializers.save()
        #             return Response({'status':serializers.data,'countries':call_func})
        #     else:
        #             return Response({'status':'error'})
    elif request.method == 'GET':
        # serializer = None
        # if not new_user.is_superuser:
            
        #     queryobj=Pagesdetail.objects.filter(userid=new_user.id).all()
        #     serializer=Pagesseril(queryobj,many=True)
        # else:
        product_id=request.META['HTTP_PRODUCTID']
        queryobj=Pagesdetail.objects.get(page_id=product_id)
        serializer=Pagesseril(queryobj)
        return Response({'status':serializer.data})
        


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
        # print(new_user.is_superuser,new_user.id)
        if(new_user.is_superuser):
            queryobj=Addetails.objects.all()
            serializer=Adserial(queryobj,many=True)
        else:
            queryobj=Addetails.objects.filter(userid=new_user.id).all()
            serializer=Adserial(queryobj,many=True)
            
        return Response(serializer.data)
    if request.method == "POST":
            data_filter=None
            try:
                data_filter=Addetails.objects.get(adid=request.data['adid'])
            except Exception as e:
                pass
            # print(request.data)
            if not data_filter or data_filter == None:
                serializer=Adserial(data=request.data)
                if serializer.is_valid():
                   
                    serializer.save()
                    return Response({'status': 'Data sucessfully added'})
                else:
                    
                    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            else:
              
                serializer=Adserial(data_filter,data=request.data)
                if serializer.is_valid():
                   
                    serializer.save()
                    return Response({'stats':'updated sucessfully'})
                else:
           
                    return Response({'stats':'updated error'})
           

@api_view(['POST','GET'])
def ad_data(request):
    if request.method == 'POST':
        id=request.META['HTTP_PRODUCTID']
        country_filter=request.META['HTTP_FILTER']
        days=request.META['HTTP_DAYS']
        platform=None
        token=request.META['HTTP_AUTHORIZATION']
        userid=request.user
        # print(userid.id)
        if request.META['HTTP_PLATFORM'] == "False":
            platform=False
        else:
            platform=request.META['HTTP_PLATFORM']
        all_data=facebook_ad_details(userid.id,'POST',id,country_filter,days,platform)
       
        return Response({'status':all_data})
        # mail=token_genrator('genjilama007@gmail.com')
        # return Response({'stats':mail})
    elif request.method == "GET":
        product_id=request.META['HTTP_PRODUCTID']
        filters=request.META['HTTP_FILTERS']
        dates=request.META['HTTP_DATES']
        stats=request.META['HTTP_STATS']
        date_sort=request.META['HTTP_DATESORT']
        multimed=request.META['HTTP_MULTIMED']
        prod=Pagesdetail.objects.get(page_id=product_id)
        queryset=None
        new_date=None
        try:
            day,month,year=(str(x) for x in dates.split('/'))
            new_date=f"{year}-{month}-{day}"
        except:
            pass
        if stats != 'Default':
            if stats == 'services':
                queryset=Addetails.objects.filter(ad_info__target__contains='Web Browsers',productid=prod.id).all()
            else:
                queryset=Addetails.objects.filter(productid=prod.id).exclude(ad_info__target__contains='Web Browsers').all()
            
            
        elif filters != 'Default' and dates!= 'Default' and date_sort != 'Default' and multimed !='Default':
            print(1)
            if date_sort == 'asc':
                queryset=Addetails.objects.filter(ad_info__platform__contains=[filters],start_date__contains=new_date,productid=prod.id,mul_type__contains=multimed).order_by('-start_date').all()
            else:
                queryset=Addetails.objects.filter(ad_info__platform__contains=[filters],start_date__contains=new_date,productid=prod.id,mul_type__contains=multimed).order_by('start_date').all()
        elif filters != 'Default' and multimed !='Default':
            print(1)
            queryset=Addetails.objects.filter(ad_info__platform__contains=[filters],mul_type__contains=multimed,productid=prod.id).all()
        elif filters != 'Default' and dates!= 'Default':
            print(1)
            queryset=Addetails.objects.filter(ad_info__platform__contains=[filters],start_date__contains=new_date,productid=prod.id).all()
        elif multimed !='Default' and date_sort != 'Default':
            if date_sort == 'asc':
                queryset=Addetails.objects.filter(mul_type__contains=multimed,productid=prod.id).order_by('-start_date').all()
            else:
                queryset=Addetails.objects.filter(mul_type__contains=multimed,productid=prod.id).order_by('start_date').all()
        elif filters!= 'Default' and date_sort != 'Default':
            if date_sort == 'asc':
                queryset=Addetails.objects.filter(ad_info__platform__contains=[filters],productid=prod.id).order_by('-start_date').all()
            else:
                queryset=Addetails.objects.filter(ad_info__platform__contains=[filters],productid=prod.id).order_by('start_date').all()
        elif dates!= 'Default' and date_sort != 'Default':
            if date_sort == 'asc':
                queryset=Addetails.objects.filter(start_date__contains=new_date,productid=prod.id).order_by('-start_date').all()
            else:
                queryset=Addetails.objects.filter(start_date__contains=new_date,productid=prod.id).order_by('start_date').all()
        elif dates!= 'Default' and multimed !='Default':
            print(1)
            queryset=Addetails.objects.filter(mul_type__contains=multimed,start_date__contains=new_date,productid=prod.id).all()
        elif date_sort !='Default':
          
            if date_sort == 'asc':
                queryset=Addetails.objects.filter(productid=prod.id).order_by('-start_date').all()
            else:
                queryset=Addetails.objects.filter(productid=prod.id).order_by('start_date').all()
           
        elif filters != 'Default':
            print(2)
            queryset=Addetails.objects.filter(ad_info__platform__contains=[filters],productid=prod.id).all()
            
        elif dates!= 'Default':
            print(3)
            queryset=Addetails.objects.filter(start_date__contains=new_date,productid=prod.id).all()
         
        elif multimed!= 'Default':
           
                queryset=Addetails.objects.filter(mul_type__contains=multimed,productid=prod.id).all()
         

        else:
            print(4)
            queryset=Addetails.objects.filter(productid=prod.id).all()
           
        serializer=Adserial(queryset,many=True)
        return Response({'stats':serializer.data})
          

@api_view(['GET'])
def graph(request):
    product_id=request.META['HTTP_PRODUCTID']
    queryset=Pagesdetail.objects.get(page_id=product_id)
   
    des=ad_deserializer(queryset.id)
    filt_func=graph_func(des['conv'],queryset.id)
    adsquery=Addetails.objects.filter(end_date='No end-date',productid=queryset.id).all()
    sponsor=Addetails.objects.filter(ad_info__target__contains='Web Browsers',productid=queryset.id).all()
    # print(this_week_status)
    filt_func.update({'data':des['serializer']})
    filt_func.update({'active_ads':len(adsquery),'service_ad':len(sponsor)})
    return Response(filt_func)

@api_view(['GET'])
def date_end(request):
    blob=end_date('9465008123')
    return Response({'status':'hi'})
@api_view(['GET'])
def get_allads(request):
    queryset=Expiredads.objects.all()
    serializer=Expireserial(queryset,many=True)
    return Response({'stats':serializer.data})

@api_view(['GET'])
def try_function(request):
    product_id=request.META['HTTP_PRODUCTID']
    callfunc=geo_converter(product_id)
    return Response({'status':callfunc['array'],'start_point':callfunc['start_point'],'admin_total':callfunc['admin_total']})
@api_view(['GET'])
def ads_page_display(request):
    if request.method == 'GET':
        page_name=request.META['HTTP_PAGENAME']
        show_data=facebook_search(page_name)
        return Response({'stats':show_data})

@api_view(['GET'])
def country_list(request):
    product_id=request.META['HTTP_PRODUCTID']
    country=request.META['HTTP_COUNTRY']
    # print(product_id,country)
    call_func=None
    if country != 'All':
        new_country=pycountry.countries.search_fuzzy(country)
        # print(new_country[0])
        param=new_country[0].alpha_2
      
        call_func=country_getter(product_id,param)
    else:
        call_func=country_getter(product_id)
    return Response({'status':call_func})
@api_view(['GET'])
def social_tracker(request):
    product_id=request.META['HTTP_PRODUCTID']
    queryset=Pagesdetail.objects.get(page_id=product_id)
   
    month=request.META['HTTP_MONTH']
    week=request.META['HTTP_WEEK']
    new_date=request.META['HTTP_SELDATE']
    months=overall_analysis(queryset.id,month,week,new_date)
    return Response({'status':months})

@api_view(['GET'])
def ads_analysis(request):
    stats=request.META['HTTP_STATS']
    month=request.META['HTTP_MONTH'] 
    week=request.META['HTTP_WEEK'] 
    product_id=request.META['HTTP_PRODUCTID']
    new_month=monthly_analysis(month) 
    new_prod=Pagesdetail.objects.get(page_id=product_id)
    newarr={'week1':{'total':0,'facebook':0,'instagram':0},'week2':{'total':0,'facebook':0,'instagram':0},'week3':{'total':0,'facebook':0,'instagram':0},'week4':{'total':0,'facebook':0,'instagram':0},'week5':{'total':0,'facebook':0,'instagram':0}}
    check_month=f"0{new_month}" 
   
    if stats != 'weekly':
        queryset=Adstracker.objects.filter(month=check_month).all()
        serializer=Adsseril(queryset,many=True)
        json_d=json.dumps(serializer.data)
        conv=json.loads(json_d)
        for i in range(len(conv)):
            if new_prod.id == conv[i]['adid']['productid']['id']:
           
                if conv[i]['weekday'] == '1':
                        newarr['week1']['total']+=1    
                        if len(conv[i]['adid']['ad_info']['platform']) > 1:
                            newarr['week1']['facebook']+=1
                            newarr['week1']['instagram']+=1
                        elif conv[i]['adid']['ad_info']['platform'][0] == 'facebook':
                            newarr['week1']['facebook']+=1
                        else:
                            newarr['week1']['instagram']+=1                  
                elif conv[i]['weekday'] == '2':
                        newarr['week2']['total']+=1
                        if len(conv[i]['adid']['ad_info']['platform']) > 1:
                            newarr['week2']['facebook']+=1
                            newarr['week2']['instagram']+=1
                        elif conv[i]['adid']['ad_info']['platform'][0] == 'facebook':
                            newarr['week2']['facebook']+=1
                        else:
                            newarr['week2']['instagram']+=1
                elif conv[i]['weekday'] == '3':
                        newarr['week3']['total']+=1
                        if len(conv[i]['adid']['ad_info']['platform']) > 1:
                            newarr['week3']['facebook']+=1
                            newarr['week3']['instagram']+=1
                        elif conv[i]['adid']['ad_info']['platform'][0] == 'facebook':
                            newarr['week3']['facebook']+=1
                        else:
                            newarr['week3']['instagram']+=1
                elif conv[i]['weekday'] == '4':
                        newarr['week4']['total']+=1
                        if len(conv[i]['adid']['ad_info']['platform']) > 1:
                            newarr['week4']['facebook']+=1
                            newarr['week4']['instagram']+=1
                        elif conv[i]['adid']['ad_info']['platform'][0] == 'facebook':
                            newarr['week4']['facebook']+=1
                        else:
                            newarr['week4']['instagram']+=1
                elif conv[i]['weekday'] == '5':
                        newarr['week5']['total']+=1
                        if len(conv[i]['adid']['ad_info']['platform']) > 1:
                            newarr['week5']['facebook']+=1
                            newarr['week5']['instagram']+=1
                        elif conv[i]['adid']['ad_info']['platform'][0] == 'facebook':
                            newarr['week5']['facebook']+=1
                        else:
                            newarr['week5']['instagram']+=1
        return Response({'status':newarr})
    else:
          queryset=Adstracker.objects.filter(month=check_month,weekday=week).all()
          serializer=Adsseril(queryset,many=True)
          json_d=json.dumps(serializer.data)
          conv=json.loads(json_d)
         
          newobj={}
          datearr=[]
          year=conv[0]['year']
          month=conv[0]['month']
          date=conv[0]['date']
          pend=pendulum.parse(f"{year}-{month}-{date}")
          today = datetime.now().date()
          start = pend.start_of('week').date()
          end = pend.end_of('week')
        
          for i in range(7):
            new_date=start+timedelta(days=i)
            curr_date=new_date.strftime("%d")
            datearr.append(curr_date)
            face="faecbook"
            insta="instagram"
            newobj.update({curr_date:{'total':0,face:0,insta:0}})
          
          for i in range(len(conv)):
           
            if new_prod.id == conv[i]['adid']['productid']['id']:
                if conv[i]['date'] in datearr:
                    
                    dg=conv[i]['date']
                   
                    newobj[dg]['total']+=1
                    fb="faecbook"
                    ins="instagram"
                    
                    if len(conv[i]['adid']['ad_info']['platform']) > 1:
                        newobj[dg][fb]+=1
                        newobj[dg][ins]+=1
                    elif conv[i]['adid']['ad_info']['platform'][0] == 'facebook':
                        newobj[dg][fb]+=1
                    else:
                        newobj[dg][ins]+=1

       
                    
        
          return Response({'status':newobj})
@api_view(['GET'])
def monthly_average(request):
    product_id=request.META['HTTP_PRODUCTID']
    query=Pagesdetail.objects.get(page_id=product_id)
    serial=Pagesseril(query) 
    geo=admin_total(serial.data)
    call_func=average_ads(query.id)
    des=ad_deserializer(query.id)
    filt_func=graph_func(des['conv'],query.id)
    adsquery=Addetails.objects.filter(end_date='No end-date',productid=query.id).all()
    sponsor=Addetails.objects.filter(ad_info__target__contains='Web Browsers',productid=query.id).all()
    video_ad=Addetails.objects.filter(mul_type__contains='video',productid=query.id).all()
    # country_func=country_getter(product_id)

    # print(country_func)
    return Response({'status':serial.data,'avg':call_func,'total_admin':geo,'top_data':filt_func,'active_ads':len(adsquery),'sponsor':len(sponsor),'video_ad':len(video_ad)})

@api_view(['GET'])
def blob(request):
    
    call=update_date()
    return Response({'status':'hi'})