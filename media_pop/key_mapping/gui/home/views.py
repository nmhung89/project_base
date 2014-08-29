from media_pop.common.base_view import BaseTemplateView, BaseJsonAjaxView
from media_pop.key_mapping.core.models import KeyMapping, SPECIAL_KEYS
import simplejson

class HomeView(BaseTemplateView):
    template_name = 'home.html'
    
    def get_data(self):
        #get all definition: because of little data, we get all definition in advance for faster lookup
        #if we have much data or other requirement, we will use ajax
        data_query_set = KeyMapping.objects.all()
        all_data = [{'SpecialKey': item.SpecialKey, 'Key': chr(int(item.Key)), 'Message': item.Message} for item in data_query_set]
        key_mapping_dict = {}
        for item in data_query_set:
            key_mapping_dict['%s_%s' % (item.SpecialKey, item.Key)] = item.Message
        key_mapping_json = simplejson.dumps(key_mapping_dict)
        keys = [(item, chr(item)) for item in range(ord('A'), ord('Z') + 1)]
        return {'key_mapping': all_data,
                'key_mapping_json': key_mapping_json,
                'keys': keys,
                'special_keys': SPECIAL_KEYS}
    
class HomeAjaxView(BaseJsonAjaxView):
    
    def input_definition(self, request, *args, **kwargs):
        rt = {'Code': 1, 'Message': 'Success'}
        special_key = request.POST.get('special_key', '')
        key = request.POST.get('key', '')
        message = request.POST.get('message', '')
        if not special_key or not key or not message:
            rt['Code'] = -1
            if not special_key:
                rt['Message'] = 'Please select special key'
            if not key:
                rt['Message'] = 'Please select key'
            if not message:
                rt['Message'] = 'Please enter message'
        else:
            #check special key, key in db
            check_rs = KeyMapping.objects.filter(SpecialKey=special_key, Key=key).exists()
            if check_rs:
                rt['Code'] = -1
                rt['Message'] = 'Your combination keys existed'
            else:
                key_mapping = KeyMapping(SpecialKey=special_key, Key=key, Message=message)
                key_mapping.save()
        
        return rt
    
    def actions(self):
        handlers = {'input-definition': self.input_definition}
        return handlers
