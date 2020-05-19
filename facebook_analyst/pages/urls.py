from django.urls import path,include
from rest_framework import routers
from.views import Displaypages,modified_get,ad_data,insert_pages

router=routers.DefaultRouter()
router.register('pages',Displaypages)


urlpatterns = [
   path('',include(router.urls)),
   path('try/',modified_get),
   path('newtry/',ad_data),
   path('secondtry/<int:id>',insert_pages),

  
]

