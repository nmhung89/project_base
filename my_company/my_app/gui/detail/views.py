from my_company.common.base_view import BaseTemplateView, BaseJsonAjaxView

class DetailView(BaseTemplateView):
    template_name = 'home_index.html'
    
    def get_data(self):
        '''transfer variables to html'''
        data = {'var1': self.request.GET.get('var1', 'blank')}
        return data
    
class DetailAjaxView(BaseJsonAjaxView):
    
    def sample1(self, *args, **kwargs):
        return {'Message01': 'I am very well, thank you'}
    
    def actions(self):
        handlers = {'sample1': self.sample1}
        return handlers