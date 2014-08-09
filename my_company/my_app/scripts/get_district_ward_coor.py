import env
from my_company.common.api_handler import ApiHandler
from my_company.my_app.core.models import District, Ward
import simplejson


g_key = 'AIzaSyCkHT4GIJ8SHs0z5VOChJIUolz8_OtHWNM'

url = 'https://maps.googleapis.com/maps/api/geocode/json'

city = ', Ho Chi Minh, Vietnam'

if __name__ == '__main__':
    list_district = District.objects.all().order_by('Order')
    ds = [{'Name': item.Pre + ' ' + item.Name, 'id': item.pk} for item in list_district]
    print simplejson.dumps(ds)
    ws = {}
    for d in list_district:
        list_ward = Ward.objects.filter(District=d)
        ws[str(d.pk)] = [{'Name': item.Pre + ' ' + item.Name, 'id': item.pk} for item in list_ward]
    print simplejson.dumps(ws)
        
        
    