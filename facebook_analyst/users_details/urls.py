
from django.urls import path,include
from rest_framework import routers
from.views import signupform,displaysearch

router=routers.DefaultRouter()
router.register('register',signupform)
router.register('searchhistory',displaysearch)

urlpatterns = [
   path('',include(router.urls))
  
]