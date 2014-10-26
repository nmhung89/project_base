from django.http import HttpResponse
from django.views.generic.base import TemplateView, View
import json


class BaseTemplateView(TemplateView):
    
    def get_data(self):
        data = {}
        return data
    
    def get_context_data(self, **kwargs):
        context = super(BaseTemplateView, self).get_context_data(**kwargs)
        try:
            data = self.get_data()
            context.update(data)
        except Exception, ex:
            #notify error message for admin by email or save into database
            raise ex
        return context
    
class BaseJsonAjaxView(View):
    
    def actions(self):
        handlers = {}
        return handlers
    
    def get_data(self, request, *args, **kwargs):
        action = kwargs.get('action')
        try:
            data = self.actions().get(action)(request, *args, **kwargs)
        except Exception, ex:
            data = {'Code': -1, 'Message': str(ex)}
        if data.get('Code', '') == '' and data.get('Message', '') == '':
            data['Code'] = 1
            data['Message'] = 'Success'
        return data
    
    def get(self, request, *args, **kwargs):
        self.method = 'GET'
        resp = self.get_data(request, *args, **kwargs)
        return HttpResponse(json.dumps(resp), content_type="application/json" )
    
    def post(self, request, *args, **kwargs):
        self.method = 'POST'
        resp = self.get_data(request, *args, **kwargs)
        return HttpResponse(json.dumps(resp), content_type="application/json" )
    
    def put(self, request, *args, **kwargs):
        self.method = 'PUT'
        resp = self.get_data(request, *args, **kwargs)
        return HttpResponse(json.dumps(resp), content_type="application/json" )
    
    def delete(self, request, *args, **kwargs):
        self.method = 'DELETE'
        resp = self.get_data(request, *args, **kwargs)
        return HttpResponse(json.dumps(resp), content_type="application/json" )