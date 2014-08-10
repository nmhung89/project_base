import uuid

from django.conf import settings
from django.contrib.gis.db import models as gismodels
from django.contrib.gis.geos import Point

from my_company.common.base_view import BaseTemplateView, BaseJsonAjaxView
from my_company.my_app.core import models
from my_company.my_app.core.models import House, HouseStatus, HouseSource,\
    HouseImage, ImageType


class CreateHouseView(BaseTemplateView):
    template_name = 'submit_property.html'
    
    def get_data(self):
        data = {'HouseTypes': models.HouseType.choices}
        return data
    
class CreateHouseAjaxView(BaseJsonAjaxView):
    
    def save_house(self, request, *args, **kwargs):
        params = request.POST
        
        htype = params.get('house-type', '').strip()
        description = params.get('house-description', '').strip()
        district = params.get('house-district', '').strip()
        ward = params.get('house-ward', '').strip()
        address = params.get('house-address', '').strip()
        num_bedroom = params.get('house-num-bedroom', '').strip()
        num_toalet = params.get('house-num-toalet', '').strip()
        phone = params.get('house-phone', '').strip()
        price = params.get('house-price', '').strip()
        electric_price = params.get('house-electric-price', '').strip()
        water_price = params.get('house-water-price', '').strip()
        size= params.get('house-size', '').strip()
        
        #boolean
        air_condition = True if params.get('house-air-condition', '') else False
        balcony = True if params.get('house-balcony', '') else False
        free_time = True if params.get('house-free-time', '') else False
        private_gate = True if params.get('house-private-gate', '') else False
        can_cook = True if params.get('house-can-cook', '') else False
        internet = True if params.get('house-internet', '') else False
        tivi_cable = True if params.get('house-tivi-cable', '') else False
        quiet = True if params.get('house-quiet', '') else False
        interior = True if params.get('house-interior', '') else False
        private_toalet = True if params.get('house-private-toalet', '') else False
        
        lat = params.get('lat', '')
        lon = params.get('lon', '')
        
        house = House()    
        house.Type = htype
        house.Status = HouseStatus.CHUA_THUE
        house.Source = HouseSource.WEB
        
        #Description
        house.Size = size
        house.BedRooms = num_bedroom
        house.Price = price
        house.ElectricityPrice = electric_price
        house.WaterPrice = water_price
        
        house.HasFurniture = interior
        house.HasInternet = internet
        house.IsFreeTime = free_time
        house.IsSeperateGate = private_gate
        house.Description = description
        #Address
        house.Phone = phone
        house.Address = address
        house.Ward_id = ward
        house.Toalets = num_toalet
        house.HasAirCondition = air_condition
        house.HasBalcony = balcony
        house.CanCook = can_cook
        house.HasTvCable = tivi_cable
        house.IsQuiet = quiet
        house.HasPrivateToalet = private_toalet
        if lat and lon:
            lat = float(lat)
            lon = float(lon)
        location = Point((lat, lon))  #lat, long
        house.Coordinate = location
        house.save()
        
        for f in request.FILES:
            file_name = self._handle_uploaded_file(request.FILES[f])
            house_image = HouseImage()
            house_image.House = house
            house_image.Type = ImageType.ORIGINAL
            house_image.Name = file_name
            house_image.save()
        
        return {'Message01': 'I am very well, thank you'}
    
    def _handle_uploaded_file(self, f):
        file_name = str(uuid.uuid4()) + '.' + f._name[-3:]
        file_path = settings.UPLOADED_FILES + file_name
        with open(file_path, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        return file_name
            
    def actions(self):
        handlers = {'save-property': self.save_house}
        return handlers