import json,lxml
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from .models import Pagesdetail
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



def facebook_ad_details(token,userid,id='9465008123',country_filter='ALL',days='lifetime',platform=False):
    
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
            image=None
            if len(content) ==0:
                image=image_parent['images'][0]['original_image_url']
            else:
                image=content[0]['original_image_url']
            platform=child[0]['publisherPlatform'][0]
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
            ad_info=json.dumps(new_ad_info)
            newobj=[{"adid":adid,"start_date":start_date,"end_date":end_date,"ad_info":new_ad_info}]
            if len(newarr) < 1:
                newarr=newobj
            else:
                newarr.extend(newobj)
            headers={
                'Authorization':token
            }
            new_data=[{"adid":adid,"start_date":start_date,"end_date":end_date,"ad_info":ad_info,"productid":productid[0].id,"userid":userid}]
            requests.post(url='http://127.0.0.1:8000/try/',data=new_data[0],headers=headers)
            # print(ad_info,'hi',newobj[0]['ad_info'])
            # print(newobj[0]['ad_info'])
            
        
        except Exception as e:
            pass
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

   


