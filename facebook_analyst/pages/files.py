import json,lxml
import requests
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
from django.core.mail import send_mail
import jwt
import os
from django.conf import settings
from datetime import date
import pendulum
from geopy.geocoders import Nominatim
from.serializers import Pagesseril,Adserial,Expireserial,Socialmedia_seril,Adsseril
from .models import Addetails,Pagesdetail,Expiredads,Socialmedia_tracker,Adstracker
from operator import itemgetter
import pycountry
import re
from time import strptime


json_fl=os.path.join('data','allcountry.json')
payload = { 
                '__user': '0',
                '__a': '1',
                '__dyn': '7xeUmBwjbgydwn8K2WnFwn84a2i5U4e1FxebzEdF8aUuxa1ZzEeUhwVwgU3ex60Vo1upE4W0OE2WxO0SobEa8465o-cw5MKi8wl8G0jx0Fwwx-2y0Mo6i58W4Utw9W7E5i17wdq7e0zEtx-',
                '__csr': '',
                '__req': '1',
                '__beoa': '0',
                '__pc': 'PHASED:DEFAULT',
                'dpr':' 1.5',
                '__ccg': 'GOOD',
                '__rev': '1002107209',
                '__s': 'irjsxb:3obywk:97f45u',
                    '__hsi': '6825235929009682906-0',
                    '__comet_req': '0',
                    'fb_dtsg': 'AQH6ya5gp5L7:AQFzoOR1Sl3i',
                    'jazoest': '22006',
                    '__spin_r': '1002107209',
                    '__spin_b': 'trunk',
                    '__spin_t': '1589087679'
                }
headers={'authority': 'www.facebook.com',
                    'method': 'POST',           
                    'scheme': 'https',
                    'accept': '*/*',
                    'accept-language': 'en-US,en;q=0.9',
                    'cookie': 'sb=iNG4XsSH_MYIO1C1NAm2GkPc; fr=1ltKALS9jzTMV9Gu0..BeuNGI.eG.AAA.0.0.BeuNGO.AWUz902B; _fbp=fb.1.1589170576959.1785962404; datr=jtG4Xs7ZT9tr5DLHA6H-4X1Q; dpr=1.25; wd=1536x294',
                    'origin': 'https://www.facebook.com',
                    'referer': 'https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=ALL&impression_search_field=has_impressions_lifetime&view_all_page_id=9465008123&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
                    'viewport-width': '767',}

def facebook_json(url):
    r = requests.post(
                url=url,
                data=payload,
                headers=headers
            )

    soup = BeautifulSoup(r.text,'lxml')
    art=soup.find('p').text
    newsplit=art.split("(;;);")
    
    new_data=newsplit[1]
    
    # ret=re.sub(r'(a-z|\s)+"',"",new_data)
    # new_ret=re.sub(r'(\w+|\s+)"(a-z|\s)',r'\1\3',ret)
    # # print(ret)
    json_data=None
    try:
        json_data=json.loads(new_data)
       
        
    except Exception as e:
        pass
    return json_data


def facebook_ad_details(userid,stats="Return",ids='9465008123',country_filter='ALL',days='lifetime',platform=False):
    
    url=None
    if not platform:
        url=f'https://www.facebook.com/ads/library/async/search_ads/?session_id=dc2f0027-ea5d-4ad1-ba9a-cd9b5bbe5011&count=500&active_status=all&ad_type=all&countries[0]={country_filter}&impression_search_field=has_impressions_{days}&view_all_page_id={ids}&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped'
    else:
        url=f'https://www.facebook.com/ads/library/async/search_ads/?session_id=dc2f0027-ea5d-4ad1-ba9a-cd9b5bbe5011&count=30&active_status=all&ad_type=all&countries[0]={country_filter}&impression_search_field=has_impressions_{days}&view_all_page_id={ids}&publisher_platforms[0]={platform}&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped'
    print(id)
    json_data=facebook_json(url)
    if json_data == None:
        print('e')
        return False
    else:
        parentclass=json_data['payload']['results']
        
        newarr=[]
        prod=Pagesdetail.objects.get(page_id=ids)
        if stats == 'Length':
        
            return (len(parentclass))
        else:
         
            for child in parentclass:
                
                    adid=child[0]['adArchiveID']
                    
                    code_date=child[0]['startDate']
                    new_date=datetime.fromtimestamp(code_date)
                    start_date=new_date.strftime("%Y-%m-%d, %H:%M:%S")
                    end_date=None
                    if child[0]['endDate'] == None:
                        end_date="No end-date"
                    else:
                        end_date=child[0]['endDate']
                    image_parent=child[0]['snapshot']
                    content=image_parent['cards']
                    video=image_parent['videos']
                    unformatted_creation_time=image_parent['creation_time']
                    date_conv=datetime.fromtimestamp(unformatted_creation_time)
                    created_time=date_conv.strftime("%d/%m/%Y, %H:%M:%S")
                    mul_type='image'
                    mul_type_link='No Link'
                    image='No img'
                    print(adid,prod.id)
                    
                    try:
                        if len(video) >=1:
                            mul_type='video'
                            image=video[0]['video_preview_image_url']
                            mul_type_link=video[0]['video_sd_url']
                        elif len(content) ==0:
                           
                            image=image_parent['images'][0]['original_image_url']
                        elif 'video_preview_image_url' in content[0]:
                            mul_type='video'
                            image=content[0]['video_preview_image_url']
                            mul_type_link=content[0]['video_sd_url']

                        else:
                           
                            image=content[0]['original_image_url']
                    except Exception as e:
                         print(e) 
                    print(mul_type_link)
                    platform=child[0]['publisherPlatform']
                    active_status=str(child[0]['isActive'])
                    parent_owner=child[0]['pageName']
                    
                    owner=parent_owner.split(".")[0]
                    target=None
                    discription=None
                    pagename=child[0]['pageName'].lower()
                    weburl=image_parent['caption']
                    search_date=date.today()

                    if weburl == "itunes.apple.com":
                        target="Apple Products"
                    elif  weburl == 'play.google.com':
                        target="Android Smartphones"
                    else:
                        target="Web Browsers"
                    
                    facebook_url=image_parent['page_profile_uri']
                    main_disc=image_parent['link_description']
                
                    if main_disc == None or main_disc == pagename :
                    
                        if len(content) == 0:
                            discription=image_parent['body']['markup']['__html']
                            
                        else:
                            discription=content[0]['title']
                    else:
                        discription=main_disc
                    if "\u200e" in discription:
                        discription=discription.replace("\u200e",'')
                    
                    
                    
                    new_ad_info={"discription":discription,"facebook_url":facebook_url,"target":target,"owner":owner,"platform":platform,"active_status":active_status,"image_src":image}

                    newobj=[{"adid":adid,"start_date":start_date,"end_date":end_date,"ad_info":new_ad_info,'created_time':created_time,'mul_type':mul_type,'mul_type_link':mul_type_link}]
                    if len(newarr) < 1:
                        newarr=newobj
                    else:
                        newarr.extend(newobj)
                    
                    new_data={"adid":adid,"start_date":start_date,'searched_date':search_date,"end_date":end_date,"ad_info":new_ad_info,"productid":prod.pk,"userid":userid,"created_time":created_time,'mul_type':mul_type,'mul_type_link':mul_type_link}
                    print(prod.pk,'hi')
                    if stats == "POST":
                    
                        data_filter=None
                        try:
                            data_filter=Addetails.objects.get(adid=new_data['adid'])
                        except Exception as e:
                            pass
                        # print(request.data)
                        if not data_filter or data_filter == None:
                            print(new_data)
                            serializer=Adserial(data=new_data)
                            if serializer.is_valid():
                                print('saved')
                                serializer.save()
                                
                            else:
                                print('lo',serializer.errors)
                        else:
                            print('updated')
                            serializer=Adserial(data_filter,data=new_data)
                            if serializer.is_valid():
                            
                                serializer.save()
                            
                            else:
                                print('li',serializer.errors)
                    # print(ad_info,'hi',newobj[0]['ad_info'])
                    # print(newobj[0]['ad_info'])
                    
            return newarr    
          
          
            

def facebook_ad_owner(page_id='9465008123',countries='ALL',newuser="1"):
   
    r = requests.post(
                url=f'https://www.facebook.com/ads/library/async/page_info/?countries[0]={countries}&view_all_page_id={page_id}',
                data=payload,
                headers=headers
            )
    soup = BeautifulSoup(r.text,'lxml')
    newarr=None
    # total_ads=facebook_ad_details(newuser,'Length',page_id)
    art= soup.find('p').text
    newsplit=art.split("(;;);")
    new_data=newsplit[1]
    json_data=json.loads(new_data)
    parent=json_data['payload']['pageInfo']
 
    try:
        
        instagram_followers=parent['igFollowers']
        instagram_username=parent['igUsername']
        facebook_like=parent['likes']
        page_admins=parent['pageAdminCountries']
        page_coverphoto=parent['pageCoverPhoto']
        new_date=parent['pageCreationDate']
        date_conv=datetime.fromtimestamp(new_date)
        page_created=date_conv.strftime("%d/%m/%Y, %H:%M:%S")
        page_name_changed=parent['pageNameChanges']
        page_weekly_spending=parent['pageSpendingInfo']['currentWeek']
        page_url=parent['pageURL']
        profile_photo=parent['profilePhoto']
        related_page=parent['relatedPages']
        page_name=json_data['payload']['viewAllPageName']
        search_date=date.today()
        
       
        # socialmedia=json.dumps()
        # page_info=json.dumps()
        newobj={"page_id":page_id,"page_name":page_name,"searched_date":search_date,'total_ads':1,"socialmedia":{'instagram_followers':instagram_followers,'instagram_username':instagram_username,'facebook_like':facebook_like},"page_info":{'page_admins':page_admins,'page_coverphoto':page_coverphoto,'page_created':page_created,'page_name_changed':page_name_changed,'page_weekly_spending':page_weekly_spending,'page_url':page_url,'profile_photo':profile_photo,'related_page':related_page}}
        newarr=newobj
        
    except Exception as e:
        print(e)
    
    return newarr


def facebook_search(name='Amazon',search='ALL'):
    url=f"https://www.facebook.com/ads/library/async/search_typeahead/?ad_type=all&country={search}&is_mobile=false&q={name}&session_id=0e6f496f-c6cb-4673-afa9-e4413dd28e8a"
    json_data=facebook_json(url)
    
    parent=json_data['payload']
    all_data=parent['pageResults']
    default_id=all_data[:5]
    # print(default_id)
    # fb_ad = facebook_ad_details(default_id) 
   
    return default_id
def country_getter(id,country='ALL'):

    url=f'https://www.facebook.com/ads/library/async/search_filters/?session_id=485cbe95-9241-4274-b818-c7a3d2373f5e&group_by_modes[0]=1&group_by_modes[1]=2&group_by_modes[2]=6&active_status=all&ad_type=all&country={country}&impression_search_field=has_impressions_lifetime&page_ids[0]={id}&view_all_page_id={id}'
    json_data=facebook_json(url)
    parent=json_data['payload']
   
    newarr=[]
    if country == 'ALL':
        new_obj=json_data['payload']['3']
        all_keys=list(new_obj.keys())
        for i in range(len(all_keys)):
            blob=pycountry.countries.get(alpha_2=all_keys[i])
            newarr.append(blob.name)
           
    else:
        new_obj=parent['6']
        
        for key,val in new_obj.items():
           
            newobj={'state':key,'ads':val['count']}
            newarr.append(newobj)
            
    return newarr

def email_sender(newemail):
    # send_mail('Account verification','Please click on the link for account verification','magaranub@gmail.com',[newemail])
  
    return 'done'

def token_genrator(email):
    obj={'email':email,'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=5)}
    secret=settings.SECRET_KEY
    token=jwt.encode(obj,secret,algorithm='HS256')
    bla=token_decoder(token)

    return token
def token_decoder(token):
    secret=settings.SECRET_KEY
    decoded=jwt.decode(token,secret,algorithm='HS256')
  
    return decoded


def week_filter(count,day):
    amount=0
    if(day  >= ((count-1) * 7) and day <=(count*7)):
            # print(count)
            amount+=1
    else:
            return False
    return amount
        
def current_week_filter(day):
    count = 1 
    while (count <= 5):
        week=week_filter(count,day)
        if not week:
            count+=1
        else:
            break
    return count

def graph_func(obj,id):
    curr_date=date.today()
    newyear,newmonth,newday=( str(x) for x in str(curr_date).split("-"))
    # print(newyear , newmonth , newday)
    new_weekday=pendulum.parse(f"{newyear}-{newmonth}-{newday}")
    curr_weekday=new_weekday.week_of_month
    # curr_day=newday
    current_week=0
    previous_week=0
    this_week_status=''
    android=0
    webbrowser=0
    apple=0
    facebook=0
    instagram=0
    messenger=0
    top_device=None
    top_platform=None
    monthly_average=average_ads(id)
   
    for newdata in range(len(obj)):
        
        ad_target=obj[newdata]['ad_info']['target']
        new_date=obj[newdata]['start_date'].split(",")[0]
        # print(new_date,curr_date)
        year,month,day=( x for x in new_date.split("-"))
        toconv_weekday=pendulum.parse(f"{year}-{month}-{day}")
        data_weekday=toconv_weekday.week_of_month
        print(month,newmonth,'hi')
        if newyear == year and newmonth == month:
            if curr_weekday == data_weekday:
                current_week+=1
            elif data_weekday == (int(curr_weekday) -1):
                previous_week+=1
        
        if ad_target == 'Web Browsers':
            webbrowser+=1
        elif ad_target == 'Apple Products':
            apple+=1
        else:
            android+=1
        platform=obj[newdata]['ad_info']['platform']

        if len(platform) >= 3:
            facebook+=1
            instagram+=1
            messenger+=1
        elif "facebook" and "instagram" in platform:
            facebook+=1
            instagram+=1
        elif "facebook" and "messenger" in platform:
            facebook+=1
            messenger+=1 
        elif "messenger" and "instagram" in platform:
            messenger+=1
            instagram+=1
        elif 'facebook' in platform:
            facebook+=1
        elif "messenger" in platform:
            messenger+=1
        else:
            instagram+=1
        # print(previous_week,current_week)
    if previous_week < current_week:
        this_week_status='Increment'
    elif previous_week == curr_weekday:
        this_week_status='Neutral'
    else:
        this_week_status='Decrement'
    if facebook>=instagram and facebook>=messenger:
        top_platform="Facebook"
    elif messenger>=facebook and messenger>=instagram:
        top_platform="Messenger"
    else:
        top_platform="Instagram"
    if apple >= webbrowser and apple >= android:
        top_device='apple'
    elif android >= webbrowser and android >= apple:
        top_device='android'
    else:
        top_device='webbrowser'

    total=(facebook+messenger+instagram)
    target_total=(android+webbrowser+apple)
    ad_target_obj={'targets':{'apple':apple,'webbrowser':webbrowser,'android':android},'top_device':top_device,'total_target':target_total}
    platform_obj={'top_platform':top_platform,'platform':{'facebook':facebook,'messenger':messenger,'instagram':instagram},'total':total}
    return({'curr_week_ads': current_week,'prev_week_ad':previous_week,'curr_ad_status':this_week_status,'ad_target':ad_target_obj,'platforms':platform_obj,'avg':monthly_average})

def ad_deserializer(id):
    queryobj=Addetails.objects.filter(productid_id=id).all()
    serializer=Adserial(queryobj,many=True)
    jsoned=json.dumps(serializer.data)
    conv=json.loads(jsoned)
    
    return {'conv':conv,'serializer':serializer.data}
def end_date(product):
    product_id=Pagesdetail.objects.get(page_id=product)

    conv_data=ad_deserializer(product_id.id)['conv']
 
    count=0
    new_count=0
    
    real_time_data=facebook_ad_details(0,1)
    newarr=list(map(itemgetter('adid'),real_time_data))
    expired_ad=[]
    curr_date=date.today()
    new_date=curr_date.strftime('%d-%m-%Y')
    # print(conv_data)
    for i in range(len(conv_data)):
        
        conv_data[i]['end_date']=new_date
      
        if conv_data[i]['adid'] not in newarr:
            conv_data[i]['end_date']=new_date
            newobj={'adsid':conv_data[i]['id'],'productid':conv_data[i]['productid']}
           
            # queryobj=None
            # try:
            #     queryobj=Expiredads.objects.filter(adsid_id=conv_data[i]['id'])
            # except Exception as e:
            #     pass
            # if not queryobj or queryobj == None:
            #     serializer=Expireserial(data=newobj)
            #     if serializer.is_valid():
            #             print('hop')
            #             serializer.save()
                        
            #     else:
            #         print(serializer.errors)
         
            queryset=Addetails.objects.get(adid=conv_data[i]['adid'])
            adserial=Adserial(queryset,conv_data[i])
            if adserial.is_valid():
                    adserial.save()
            else:
                    print(adserial.errors)
            
           
           
        else:
            count+=1
    # obu={'bla':'lop'}
    # obu['bla']='kl'
    # print(obu)
    return 'hi'

# end_date(9465008123)
def geo_identifier(name):
    geo_data=None
    with open('allcountry.json','r') as json_file:
        new_json=json.load(json_file)
        filt_json=new_json['features']
        for country in range(len(filt_json)):
            # print(filt_json[country]["properties"]['A3'])
            if filt_json[country]["properties"]['A3'] == name:
                geo_data= filt_json[country]
    return geo_data 

def lat_long_getter(string):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location=geolocator.geocode(string)
    new_lat=location.latitude
    new_lon=location.longitude
    obj={'latitude':new_lat,'longitude':new_lon}
    return obj
def admin_total(obj):
    jsoned=json.dumps(obj)
    conv=json.loads(jsoned)
    admins=conv['page_info']['page_admins']
    new_split=admins.split(",")
    new_tot=0
    main_target=None
    for count_data in range(len(new_split)):
        data_split=(new_split[count_data]).rsplit(" ",1)
        old_total=data_split[1].replace(")","").split("(")[1]
        new_total=int(old_total)
        new_tot+=new_total
        
       
    # all_tot=list(map(itemgetter('total'),newarr))
    # admin_total=sum(all_tot)
    # # print(admin_total)
   
    return (new_tot)

    
    

def geo_converter(pgid):
    queryobj=Pagesdetail.objects.get(page_id=pgid)
    serializer=Pagesseril(queryobj)
    jsoned=json.dumps(serializer.data)
    conv=json.loads(jsoned)
    admins=conv['page_info']['page_admins']
    newarr=[]
    new_split=admins.split(",")
    new_tot=0
    main_target=None
    for count_data in range(len(new_split)):
        data_split=(new_split[count_data]).rsplit(" ",1)
        new_data=data_split[0]
        country_name=pycountry.countries.search_fuzzy(new_data)
        alpha=country_name[0].alpha_3
        geo_converted=geo_identifier(alpha)
        old_total=data_split[1].replace(")","").split("(")[1]
        new_total=int(old_total)
        lat_long_data=lat_long_getter(new_data)
        geo_converted.update(lat_long_data)
        

        geo_converted.update({'countryname':new_data,'total':new_total})
        if new_total > new_tot:
            new_tot=new_total
            main_target=lat_long_data
        else:
            pass
        newarr.append(geo_converted)

       
    all_tot=list(map(itemgetter('total'),newarr))
    admin_total=sum(all_tot)
    # print(admin_total)

    
    ret_obj={'array':newarr,'start_point':main_target,'admin_total':admin_total}
    return ret_obj



def page_getter(product_id,country,new_user):
        call_func=country_getter(product_id)
        filter_data=None
        try:  
            filter_data=Pagesdetail.objects.get(page_id=product_id)
        except Exception as e:
            pass
        serializers=None
        if not filter_data or filter_data == None:
            prod_func=facebook_ad_owner(product_id,country,new_user)
            serializers=Pagesseril(data=prod_func)
            if serializers.is_valid():
                serializers.save()
            else:
                print(serializers.errors)
            return {'status':serializers.data,'countries':call_func}
        else:
            prod_func=facebook_ad_owner(product_id,country,new_user)
          
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
                new_instagram_followers=None
                if old_instagram_followers == None or old_instagram_followers== 'null':
                    new_instagram_followers="No Connected Instagram Page"
                else:
                    new_instagram_followers=prod_func['socialmedia']['instagram_followers'] - filter_data.socialmedia['instagram_followers']
                instagram_status=None
                old_facebook_like=filter_data.socialmedia['facebook_like']
                new_facebook_like=prod_func['socialmedia']['facebook_like'] - filter_data.socialmedia['facebook_like']
                facebook_status=None
                if new_instagram_followers == "No Connected Instagram Page":
                    instagram_status="No Instagramm data"
                else:
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
                
                data={
                    'fb_likes':prod_func['socialmedia']['facebook_like'],
                    'insta_likes':prod_func['socialmedia']['instagram_followers'],
                    'fb_stats':new_facebook_like,
                    'insta_stats':new_instagram_followers,
                    'date':date.today(),
                    'productid':filter_data.id
                }
                
                track_seril=Socialmedia_seril(data=data)
                if track_seril.is_valid():
                    track_seril.save()
                else:
                    print(track_seril.errors)
               
            else:
                instagram_data=filter_data.insatgram_tracker
                facebook_data=filter_data.facebook_tracker
               
            instagram={'insatgram_tracker':instagram_data}
            facebook={'facebook_tracker':facebook_data}
            prod_func.update(facebook)
            prod_func.update(instagram)
           
            
            serializers=Pagesseril(filter_data,data=prod_func)
            if serializers.is_valid():
                    serializers.save()
                    return {'status':serializers.data,'countries':call_func}
            else:
                    return {'status':'error'}


def adstracker_data(product_id):
    prod_queryset=Pagesdetail.objects.get(page_id=product_id)
    ad_data=ad_deserializer(prod_queryset.id)
    conv_data=ad_data['conv']
    
    for i in range(len(conv_data)):
       
        new_date=conv_data[i]['start_date'].rsplit(',')[0]
        year, month, day =(str(x) for x in new_date.split('-'))
        weekday_parse=pendulum.parse(f"{year}-{month}-{day}")
        weekday=weekday_parse.week_of_month
        object_fill=None
        try:
            object_fill=Adstracker.objects.get(adid=conv_data[i]['id'])
        except Exception as e:
            pass
      
        if object_fill == None :
            print(conv_data[i]['id'])
            try:
                data={
                    'year':year,
                    'month':month,
                    'date':day,
                    'weekday':weekday,
                    'adid':conv_data[i]['id']
                }
                print(data)
                serializer=Adsseril(data=data)
                if serializer.is_valid():
                    print('yoo')
                    serializer.save()
                else:
                    print(serializer.errors)
            except Exception as e:
                print(e)
        
        
    return 'hi'




def timeout():
    queryobj=Pagesdetail.objects.all()
    serializer=Pagesseril(queryobj,many=True)
    jsoned=json.dumps(serializer.data)
    conv=json.loads(jsoned)
    print('runned')
    for i in range(len(conv)):
    

        page_getter(conv[i]['page_id'],'ALL','1')
        adstracker_data(conv[i]['page_id'])
        facebook_ad_details(1,'POST',conv[i]['page_id'])
    return 'hi'

def monthly_analysis(month):
    month_converter=strptime(month,'%b').tm_mon

    return month_converter

def overall_analysis(product_id,month,week='Default',date='Default'):  
    queryset=Socialmedia_tracker.objects.filter(productid=product_id).all()
    srializer=Socialmedia_seril(queryset,many=True)
    json_du=json.dumps(srializer.data)
    conv=json.loads(json_du)
    sendarr=None
    if week != 'Default':
        searched_month=monthly_analysis(month)
        newobj={'facebook_like':{},'instagram_like':{}}
        for i in range(len(conv)):
            year,newmonth,day=(str(x) for x in conv[i]['date'].split("-"))
           
           
            if newmonth == str(f"0{searched_month}"):
              
                new_weekday=pendulum.parse(f"{year}-{newmonth}-{day}")
                curr_weekday=new_weekday.week_of_month
                
                if str(curr_weekday) == week:
                    new_date=datetime(int(year),int(newmonth),int(day))
                    curr_day=new_date.strftime("%a")
                  
                    newobj['facebook_like'].update({curr_day:conv[i]['fb_stats']})
                    newobj['instagram_like'].update({curr_day:conv[i]['insta_stats']})
                    
                   
                else:
                    print(curr_weekday)
        sendarr=newobj
      
    elif date != 'Default':
        newobj={'facebook_like':'','instagram_like':''}
        for i in range(len(conv)):
            if conv[i]['date'] == str(date):
                newobj['facebook_like']=conv[i]['fb_stats']
                newobj['instagram_like']=conv[i]['insta_stats']
        

        sendarr=newobj
    else:
            searched_month=monthly_analysis(month)
            newobj={'facebook_like':{'week1':0,'week2':0,'week3':0,'week4':0,'week5':0},'instagram_like':{'week1':0,'week2':0,'week3':0,'week4':0,'week5':0}}
            for i in range(len(conv)):
                year,newmonth,day=(str(x) for x in conv[i]['date'].split("-"))
                if newmonth == str(f"0{searched_month}"):
                    new_weekday=pendulum.parse(f"{year}-{newmonth}-{day}")
                    curr_weekday=new_weekday.week_of_month
                    print(curr_weekday,conv[i]['insta_stats'])
                    if curr_weekday == 1:
                        newobj['facebook_like']['week1']+=int(conv[i]['fb_stats'])
                        newobj['instagram_like']['week1']+=int(conv[i]['insta_stats'])
                    elif curr_weekday == 2:
                        newobj['facebook_like']['week2']+=int(conv[i]['fb_stats'])
                        newobj['instagram_like']['week2']+=int(conv[i]['insta_stats'])
                    elif curr_weekday == 3:
                        newobj['facebook_like']['week3']+=int(conv[i]['fb_stats'])
                        newobj['instagram_like']['week3']+=int(conv[i]['insta_stats'])
                    elif curr_weekday == 4:
                        newobj['facebook_like']['week4']+=int(conv[i]['fb_stats'])
                        newobj['instagram_like']['week4']+=int(conv[i]['insta_stats'])
                    elif curr_weekday == 5:
                        newobj['facebook_like']['week5']+=int(conv[i]['fb_stats'])
                        newobj['instagram_like']['week5']+=int(conv[i]['insta_stats'])
           
           
            sendarr=newobj        
    return sendarr
def average_ads(id):
    curr_month=datetime.now().month
    new_arr=[]

    for i in range(1,(curr_month)):
        new_month=f"0{i}"
        queryset=Adstracker.objects.filter(adid__productid=id,month=new_month).all()
        new_arr.append(len(queryset))
    total_ads=sum(new_arr)
    abv_ads=round(total_ads/len(new_arr),2)
    # print(round(abv_ads,2),total_ads,'hi',curr_month)
    query=Socialmedia_tracker.objects.filter(productid=id).all()
    srial=Socialmedia_seril(query,many=True)
    dump=json.dumps(srial.data)
    conv=json.loads(dump)
    facebook_total=0
    instagram_total=0
    new_date=datetime.now().isocalendar()[1]
    for i in range(len(conv)):
        facebook_total+=int(conv[i]['fb_stats'])
        instagram_total+=int(conv[i]['insta_stats'])
    avg_fb_weekly=round(facebook_total/new_date,2)
    avg_insta_weekly=round(instagram_total/new_date,2)
   
    newobj={'avg_monthly_ad':abv_ads,'avg_fb_weekly':avg_fb_weekly,'avg_insta_weekly':avg_insta_weekly}
    return newobj

 
def update_date():
    query=Pagesdetail.objects.all()
    seril=Pagesseril(query,many=True)
    json_d=json.dumps(seril.data)
    conv=json.loads(json_d)
    for i in range(len(conv)):
        print(conv[i]['id'])
        newquery=Addetails.objects.filter(productid=conv[i]['id']).all()
        new_seril=Adserial(newquery,many=True)
        json_do=json.dumps(new_seril.data)
        new_conv=json.loads(json_do)
        
        for j in range(len(new_conv)):
         
           
        #     new_conv[j]['start_date']=updated
           
            new_query=Addetails.objects.get(adid=new_conv[j]['adid'])
       
            new_conv[j]['mul_type_link']='No Link'
            # new_conv[j]['productid']=conv[i]['id']
            srl=Adserial(new_query,data=new_conv[j])
            if srl.is_valid():
                srl.save()
            else:
                print(srl.errors)
            
            
            
    
# def try_date(year,month,date):
   
#     # year='2020'
#     # month='06'
#     # date='04'
    
#     print(newobj,newarr)