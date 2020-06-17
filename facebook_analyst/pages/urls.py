from django.urls import path,include
from rest_framework import routers
from .views import Displaypages,modified_get,ad_data,insert_pages,graph,date_end,get_allads,try_function,ads_page_display,country_list,ads_analysis,social_tracker,monthly_average,blob
from apscheduler.schedulers.background import BackgroundScheduler
from .files import timeout
scheduler=BackgroundScheduler()
job=None
router=routers.DefaultRouter()
router.register('pages',Displaypages)


urlpatterns = [
   path('',include(router.urls)),
   path('try/',modified_get),
   path('newtry/',ad_data),
   path('secondtry/<int:id>',insert_pages),
   path('graph/',graph),
   path('end/',date_end),
   path("adsdis/",get_allads),
   path("geo/",try_function),
   path("adsdisplay/",ads_page_display),
   path("getcountry/",country_list),
   path("getsocial/",social_tracker),
   path("adanalysis/",ads_analysis),
   path('compare/',monthly_average),
   path('blob/',blob)

  
]

def start_job():
    global job
    job=scheduler.add_job(timeout,'interval',minutes=30)
    try:
        scheduler.start()
    except :
        pass
start_job()