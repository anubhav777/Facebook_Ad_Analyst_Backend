import json
from pages.models import Pagesdetail
from pages.serializers import Pagesseril
from django.conf import settings
from django.core.mail import send_mail
import jwt
import datetime
from datetime import timedelta
def admin_pages():
    queryset=Pagesdetail.objects.all()
    serial=Pagesseril(queryset,many=True)
    json_d=json.dumps(serial.data)
    conv_data=json.loads(json_d)
    print(conv_data)
    newarr=[]
    for i in range(len(conv_data)):
        print(conv_data[i]['searched_date'])
        newobj={'id':conv_data[i]['id'],'date':conv_data[i]['searched_date'],'productid':conv_data[i]}
        newarr.append(newobj)
    return newarr

def email_sender(newemail,tok):
    send_mail('Account verification',f''' to verify your account please click the link below
               http://localhost:3000/verify?={tok}
        
        ''' ,'magaranub@gmail.com',[newemail])
  
    return 'done'

def token_genrator(email):
    obj={'email':email,'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)}
    secret=settings.SECRET_KEY
    token=jwt.encode(obj,secret,algorithm='HS256')
    send_em=email_sender(email,token)
 
def token_decoder(token):
    secret=settings.SECRET_KEY
    decoded=jwt.decode(token,secret,algorithm='HS256')
  
    return decoded