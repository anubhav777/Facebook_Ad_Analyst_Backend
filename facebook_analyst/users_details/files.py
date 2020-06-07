import json
from pages.models import Pagesdetail
from pages.serializers import Pagesseril

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