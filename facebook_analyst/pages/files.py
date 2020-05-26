import json,lxml
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from django.core.mail import send_mail
import jwt
import os
from django.conf import settings
from datetime import date
import pendulum
from geopy.geocoders import Nominatim
from.serializers import Pagesseril,Adserial,Expireserial
from .models import Addetails,Pagesdetail,Expiredads
from operator import itemgetter
import pycountry
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
    json_data=json.loads(new_data)
    return json_data



def facebook_ad_details(token,userid,stats="Return",id='9465008123',country_filter='ALL',days='lifetime',platform=False):
    
    url=None
    if not platform:
        url=f'https://www.facebook.com/ads/library/async/search_ads/?session_id=dc2f0027-ea5d-4ad1-ba9a-cd9b5bbe5011&count=30&active_status=all&ad_type=all&countries[0]={country_filter}&impression_search_field=has_impressions_{days}&view_all_page_id={id}&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped'
    else:
        url=f'https://www.facebook.com/ads/library/async/search_ads/?session_id=dc2f0027-ea5d-4ad1-ba9a-cd9b5bbe5011&count=30&active_status=all&ad_type=all&countries[0]={country_filter}&impression_search_field=has_impressions_{days}&view_all_page_id={id}&publisher_platforms[0]={platform}&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped'
    json_data=facebook_json(url)
    parentclass=json_data['payload']['results']
    newarr=[]

    for child in parentclass:
        try:
            adid=child[0]['adArchiveID']
            code_date=child[0]['startDate']
            new_date=datetime.fromtimestamp(code_date)
            start_date=new_date.strftime("%d/%m/%Y, %H:%M:%S")
            end_date=None
            if child[0]['endDate'] == None:
                end_date="No end-date"
            else:
                end_date=child[0]['endDate']
            image_parent=child[0]['snapshot']
            content=image_parent['cards']
            unformatted_creation_time=image_parent['creation_time']
            date_conv=datetime.fromtimestamp(unformatted_creation_time)
            created_time=date_conv.strftime("%d/%m/%Y, %H:%M:%S")
            image=None
            if len(content) ==0:
                image=image_parent['images'][0]['original_image_url']
            else:
                image=content[0]['original_image_url']
            platform=child[0]['publisherPlatform']
            active_status=str(child[0]['isActive'])
            parent_owner=child[0]['pageName']
            owner=parent_owner.split(".")[0]
            target=None
            discription=None
            pagename=child[0]['pageName'].lower()
            weburl=image_parent['caption']
            if weburl == "itunes.apple.com":
                target="Apple Products"
            elif  weburl == 'play.google.com':
                target="Android Smartphones"
            else:
                target="Web Browsers"
            facebook_url=image_parent['page_profile_uri']
            main_disc=image_parent['link_description']
            if main_disc == None or main_disc == pagename :
                discription=content[0]['title']
            else:
                discription=main_disc
            if "\u200e" in discription:
                discription=discription.replace("\u200e",'')
            productid=Pagesdetail.objects.filter(page_id=id)

            new_ad_info={"discription":discription,"facebook_url":facebook_url,"target":target,"owner":owner,"platform":platform,"active_status":active_status,"image_src":image}

            newobj=[{"adid":adid,"start_date":start_date,"end_date":end_date,"ad_info":new_ad_info,'created_time':created_time}]
            if len(newarr) < 1:
                newarr=newobj
            else:
                newarr.extend(newobj)
            headers = {
                'Authorization':token
            }
            new_data=[{"adid":adid,"start_date":start_date,"end_date":end_date,"ad_info":new_ad_info,"productid":productid[0].id,"userid":userid,"created_time":created_time}]
            if stats == "POST":
                print('po')
                # requests.post(url='http://127.0.0.1:8000/try/',data=new_data[0],headers=headers)
                data_filter=None
                try:
                    data_filter=Addetails.objects.get(adid=new_data[0]['adid'])
                except Exception as e:
                    pass
                # print(request.data)
                if not data_filter or data_filter == None:
                    serializer=Adserial(data=new_data[0])
                    if serializer.is_valid():
                        print('ho')
                        serializer.save()
                        
                    else:
                        print(serializer.errors)
                else:
                    serializer=Adserial(data_filter,data=new_data[0])
                    if serializer.is_valid():
                        print('val')
                        serializer.save()
                    
                    else:
                        print(serializer.errors)
            # print(ad_info,'hi',newobj[0]['ad_info'])
            # print(newobj[0]['ad_info'])
            
        
        except Exception as e:
            pass
    print(stats)
    return newarr

def facebook_ad_owner(page_id='9465008123',countries='ALL'):
    r = requests.post(
                url=f'https://www.facebook.com/ads/library/async/page_info/?countries[0]={countries}&view_all_page_id={page_id}',
                data=payload,
                headers=headers
            )
    soup = BeautifulSoup(r.text,'lxml')
    newarr=None
    try:
        art= soup.find('p').text
        newsplit=art.split("(;;);")
        new_data=newsplit[1]
        json_data=json.loads(new_data)
        parent=json_data['payload']['pageInfo']
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
        # socialmedia=json.dumps()
        # page_info=json.dumps()
        newobj={"page_id":page_id,"page_name":page_name,"socialmedia":{'instagram_followers':instagram_followers,'instagram_username':instagram_username,'facebook_like':facebook_like},"page_info":{'page_admins':page_admins,'page_coverphoto':page_coverphoto,'page_created':page_created,'page_name_changed':page_name_changed,'page_weekly_spending':page_weekly_spending,'page_url':page_url,'profile_photo':profile_photo,'related_page':related_page}}
        newarr=newobj
        
    except Exception as e:
        print(e)
    
    return newarr


def facebook_search(name='Amazon',search='ALL'):
    url=f"https://www.facebook.com/ads/library/async/search_typeahead/?ad_type=all&country={search}&is_mobile=false&q={name}&session_id=0e6f496f-c6cb-4673-afa9-e4413dd28e8a"
    json_data=facebook_json(url)
    
    parent=json_data['payload']
    all_data=parent['pageResults']
    default_id=all_data[0]['id']
    # print(default_id)
    fb_ad = facebook_ad_details(default_id) 
    return fb_ad

def email_sender(newemail):
    # send_mail('Account verification','Please click on the link for account verification','magaranub@gmail.com',[newemail])
    print(settings.SECRET_KEY)
    return 'done'

def token_genrator(email):
    obj={'email':email,'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=5)}
    secret=settings.SECRET_KEY
    token=jwt.encode(obj,secret,algorithm='HS256')
    bla=token_decoder(token)
    print(bla)
    return token
def token_decoder(token):
    secret=settings.SECRET_KEY
    decoded=jwt.decode(token,secret,algorithm='HS256')
    print(decoded['email'])
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

def graph_func(obj):
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
    top_platform=None
    for newdata in range(len(obj)):
        
        ad_target=obj[newdata]['ad_info']['target']
        new_date=obj[newdata]['start_date'].split(",")[0]
        # print(new_date,curr_date)
        day,month,year=( x for x in new_date.split("/"))
        toconv_weekday=pendulum.parse(f"{year}-{month}-{day}")
        data_weekday=toconv_weekday.week_of_month

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
        top_platform="facebook"
    elif messenger>=facebook and messenger>=instagram:
        top_platform="messenger"
    else:
        top_platform="instagram"
    ad_target_obj={'apple':apple,'webbrowser':webbrowser,'android':android}
    platform_obj={'top_platform':top_platform,'platform':{'facebook':facebook,'messenger':messenger,'instagram':instagram}}
    return({'curr_week_ads': current_week,'prev_week_ad':previous_week,'curr_ad_status':this_week_status,'ad_target':ad_target_obj,'platforms':platform_obj})

def ad_deserializer(id):
    queryobj=Addetails.objects.filter(productid_id=id).all()
    serializer=Adserial(queryobj,many=True)
    jsoned=json.dumps(serializer.data)
    conv=json.loads(jsoned)
    
    return {'conv':conv,'serializer':serializer.data}
def end_date(product):
    product_id=Pagesdetail.objects.get(page_id=product)
    print(product_id.id)
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
        print(conv_data[i]['id'])
        if conv_data[i]['adid'] not in newarr:
            newobj={'adsid':conv_data[i]['id'],'productid':conv_data[i]['productid']}
            queryobj=None
            try:
                queryobj=Expiredads.objects.filter(adsid_id=conv_data[i]['id'])
            except Exception as e:
                pass
            if not queryobj or queryobj == None:
                serializer=Expireserial(data=newobj)
                if serializer.is_valid():
                        print('hop')
                        serializer.save()
                        
                else:
                    print(serializer.errors)

                queryset=Addetails.objects.get(adid=conv_data[i]['adid'])
                adserial=Adserial(queryset,conv_data[i])
                if serializer.is_valid():
                    serializer.save()
                else:
                    print(serializer.errors)
            else:
                print('already added')
           
           
        else:
            count+=1
    obu={'bla':'lop'}
    obu['bla']='kl'
    print(obu)
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

def geo_converter():
    queryobj=Pagesdetail.objects.filter(pk=1).all()
    serializer=Pagesseril(queryobj,many=True)
    jsoned=json.dumps(serializer.data)
    conv=json.loads(jsoned)
    admins=conv[0]['page_info']['page_admins']
    newarr=[]
    new_split=admins.split(",")
    
    for count_data in range(len(new_split)):
        data_split=(new_split[count_data]).rsplit(" ",1)
        new_data=data_split[0]
        country_name=pycountry.countries.search_fuzzy(new_data)
        alpha=country_name[0].alpha_3
        geo_converted=geo_identifier(alpha)
        old_total=data_split[1].replace(")","").split("(")[1]
        new_total=int(old_total)
        geo_converted.update({'countryname':new_data,'total':new_total})
        newarr.append(geo_converted)

       

    # print(newarr)
    return newarr

