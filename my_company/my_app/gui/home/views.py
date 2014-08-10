# -*- coding: utf-8 -*-
import simplejson

from my_company.common.base_view import BaseTemplateView, BaseJsonAjaxView
from my_company.my_app.core import models, dao
from my_company.my_app.core.models import District, Ward, House, HouseType,\
    ImageType
from django.conf import settings
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from my_company.common.utils import format_vn_currency
from my_company.common import utils

class HomeView(BaseTemplateView):
    template_name = 'index.html'
    
    def get_data(self):
        return {}
    
class HomeAjaxView(BaseJsonAjaxView):
    
    def get_house(self, request, *args, **kwargs):        
        #add new
        order_by = request.GET.get('order_by', '-CreatedTime')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 30))
        
        htype = request.GET.get('type', '')
        try:
            lat = float(request.GET.get('lat', ''))
            lon = float(request.GET.get('lon', ''))
        except:
            lat = lon = ''
        radius = request.GET.get('radius', '')
        min_radius = request.GET.get('min_radius', '')
        try:
            min_price = float(request.GET.get('min_price', '').strip())
        except:
            min_price = ''
        try:
            max_price = request.GET.get('max_price', '').strip()
        except:
            max_price = ''
        
        houses = House.objects.all()
        if order_by.find('distance') < 0:
            houses = houses.order_by(order_by)
            
        if htype:
            houses = houses.filter(Type=htype)
        if min_price:
            houses = houses.filter(Price__gte=min_price)
        if max_price:
            houses = houses.filter(Price__lte=max_price)
        if radius:
            radius = float(radius)
            center_point = Point(lat, lon)
            houses = houses.filter(Coordinate__distance_lte=(center_point, D(km=radius)))
        if min_radius:
            houses = houses.filter(Coordinate__distance_gt=(center_point, D(km=min_radius)))
        
        if lat and lon and order_by.find('distance') >= 0:
            center_point = Point(lat, lon)
            houses = houses.distance(center_point).order_by(order_by)
        
        houses = houses[(page-1)*page_size:page*page_size]
        is_continue = True if houses.__len__() == page_size else False
        
        data = {'locations': [], 'types': [], 'contents': [], 'images': [], 'details': [], 'is_continue': is_continue,
                'page': page+1}
        for house in houses:
            avatar_url = utils.get_image_url(house.images.all()[0].Name, ImageType.LARGE)
            data['locations'].append((house.Coordinate.x, house.Coordinate.y))
            data['types'].append(house.Type)
            
            image_link = '<img src="/static/assets/img/icons/house/%s.png" alt="">'
            if house.Type == HouseType.CHUNG_CU:
                data['images'].append(image_link % 'chungcu')
            elif house.Type == HouseType.NHA_NGUYEN_CAN:
                data['images'].append(image_link % 'nhanguyencan')
            elif house.Type == HouseType.NHA_TRO:
                data['images'].append(image_link % 'nhatro')
                
            formatted_price = format_vn_currency(house.Price)
            highlight = HouseType.choices[house.Type][1] + u': ' + house.Highlight
            link = '/detail/%s/' % (house.pk)
            data['contents'].append('<div class="infobox"><div class="infobox-header"><h3 class="infobox-title">' +
                                '<a href="' + link + '">' + highlight + '</a></h3></div>' +
                                '<div class="infobox-picture"><a href="' + link + '"><img src="'
                                 + avatar_url + '" alt=""></a><div class="infobox-price">'
                                 + formatted_price + '</div></div></div>')
            
            data['details'].append({'link': '/detail/%s/' % (house.pk),
                                 'street': house.Address,
                                 'district': house.District.Name if house.District else '',
                                 'type': house.Type,
                                 'price': format_vn_currency(house.Price),
                                 'img': settings.IMAGE_PATH + house.images.all()[0].Name,
                                 'size': house.Size,
                                 'bedroom': house.BedRooms,
                                 'toalet': house.Toalets
                                 })
        
        return {'HasError': False, 'data': data}
    
    def actions(self):
        handlers = {'get-house': self.get_house}
        return handlers