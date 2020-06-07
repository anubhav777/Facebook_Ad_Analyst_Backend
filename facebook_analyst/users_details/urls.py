
from django.urls import path,include
from rest_framework import routers
from.views import signupform,email_validator,reset_password,user_pages

router=routers.DefaultRouter()
router.register('register',signupform)


urlpatterns = [
   path('',include(router.urls)),
   path('verification/<email>/',email_validator),
   path('reset/<int:id>',reset_password),
   path('addpage/<int:id>',user_pages)
  
]