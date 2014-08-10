from django.conf import settings
from django.contrib.gis.geos.point import Point

from my_company.common import utils
from my_company.common.base_view import BaseTemplateView, BaseJsonAjaxView
from my_company.common.utils import format_vn_currency
from my_company.my_app.core.models import House, HouseType, Message, ImageType


class DetailView(BaseTemplateView):
    template_name = 'property_detail.html'
    
    def get_data(self, **kwargs):
        pk = kwargs.get('pk', '')
        house = House.objects.get(pk=pk)
        images = house.images.filter(Type=ImageType.LARGE)
        image_links = []
        for image in images:
            image_links.append(utils.get_image_url(image.Name, ImageType.LARGE))
        img_icon = utils.type_to_image_link(house.Type)
                                 
        data = {'pk': pk, 'house': house, 'formatted_price': format_vn_currency(house.Price),
                'highlight': HouseType.choices[house.Type][1] + u': ' + house.Highlight,
                'images': image_links,
                'img_icon': img_icon}
        return data
    
class DetailAjaxView(BaseJsonAjaxView):
    
    def get_related_house(self, request, *args, **kwargs):
        pk = request.GET.get('pk', '')
        lat = float(request.GET.get('lat'))
        lon = float(request.GET.get('lon'))
        ref_location = Point(lat, lon)
        related_house = House.objects.filter().distance(ref_location).order_by('distance')[:10]
        related_house_detail = []
        for house in related_house:
            if house.pk == pk:
                continue
            related_house_detail.append({'address': house.Address,
                                         'district': house.District.Name if house.District else '',
                                         'price': format_vn_currency(house.Price),
                                         'link': '/detail/%s/' % (house.pk),
                                         'img': utils.get_image_url(house.images.all()[0].Name, ImageType.SMALL)
                                         })
        return {'related_house': related_house_detail}
    
    def send_message(self, request, *args, **kwargs):
        content = request.POST.get('content')
        msg = Message(Content = content)
        msg.save()
    
    def actions(self):
        handlers = {'get-related-house': self.get_related_house,
                    'send-message': self.send_message}
        return handlers