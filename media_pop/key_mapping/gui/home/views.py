from media_pop.common.base_view import BaseTemplateView, BaseJsonAjaxView
from media_pop.key_mapping.core.models import KeyMapping
import simplejson

class HomeView(BaseTemplateView):
    template_name = 'home.html'
    
    def get_data(self):
        #get all definition: because of little data, we get all definition in advance for faster lookup
        #if we have much data or other requirement, we will use ajax
        all_data = KeyMapping.objects.all()
        key_mapping = [{'%s_%s' % (item.SpecialKey, item.Key): item.Message} for item in all_data]
        key_mapping_json = simplejson.dumps(key_mapping)
        keys = [chr(item) for item in range(ord('A'), ord('Z'))]
        return {'key_mapping': key_mapping,
                'key_mapping_json': key_mapping_json,
                'keys': keys}
    
class HomeAjaxView(BaseJsonAjaxView):
    
    def input_definition(self, request, *args, **kwargs):
        rt = {'Code': 1, 'Message': 'Success'}
        special_key = request.POST.get('SpecialKey', '')
        key = request.POST.get('Key', '')
        message = request.POST.get('Message', '')
        if special_key or key or message:
            rt['Code'] = -1
            if special_key:
                rt['Message'] = 'Please select special key'
            if key:
                rt['Message'] = 'Please select key'
            if message:
                rt['Message'] = 'Please enter message'
        else:
            #check special key, key in db
            check_rs = KeyMapping.objects.filter(SpecialKey=special_key, Key=key).exists()
            if not check_rs:
                rt['Code'] = -1
                rt['Message'] = 'Your combination keys existed'
            else:
                key_mapping = KeyMapping(SpecialKey=special_key, Key=key, Message=message)
                key_mapping.save()
        
        return rt
    
    def actions(self):
        handlers = {'input-definition': self.input_definition}
        return handlers