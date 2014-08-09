import simplejson

from my_company.common.base_view import BaseTemplateView, BaseJsonAjaxView
from my_company.my_app.core import models
from my_company.my_app.core.models import District, Ward


class HomeView(BaseTemplateView):
    template_name = 'index.html'
    
    def get_data(self):
        data = {'HouseTypes': models.HouseType.choices}
        return data
    
class HomeAjaxView(BaseJsonAjaxView):
    
    def sample1(self, *args, **kwargs):
        return {'Message01': 'I am very well, thank you'}
    
    def actions(self):
        handlers = {'sample1': self.sample1}
        return handlers