from django.http import HttpResponse
from django.template import loader
from django.template.context import RequestContext

from my_company.common.base_view import BaseTemplateView, BaseJsonAjaxView
from my_company.my_app.core import models


class CreateHouseView(BaseTemplateView):
    template_name = 'submit_property.html'
    
    def get_data(self):
        data = {'HouseTypes': models.HouseType.choices}
        return data
    
class CreateHouseAjaxView(BaseJsonAjaxView):
    
    def save_house(self, request, *args, **kwargs):
        params = request.POST
        house_type = params.get('house-type', '')
        return {'Message01': 'I am very well, thank you'}
    
    def actions(self):
        handlers = {'save-property': self.save_house}
        return handlers