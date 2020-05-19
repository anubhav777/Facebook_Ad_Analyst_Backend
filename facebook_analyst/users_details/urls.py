
from django.urls import path,include
from rest_framework import routers
from.views import signupform,displaysearch,email_validator,reset_password

router=routers.DefaultRouter()
router.register('register',signupform)
router.register('searchhistory',displaysearch)

urlpatterns = [
   path('',include(router.urls)),
   path('verification/<email>/',email_validator),
   path('reset/<int:id>',reset_password)
  
]