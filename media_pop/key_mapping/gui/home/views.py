from media_pop.common.base_view import BaseTemplateView, BaseJsonAjaxView
from media_pop.key_mapping.core.models import KeyMapping, SPECIAL_KEYS
import json

class HomeView(BaseTemplateView):
    template_name = 'home.html'
    
    def get_data(self):
        #get all definition: because of little data, we get all definition in advance for faster lookup
        #if we have much data or other requirement, we will use ajax
        data_query_set = KeyMapping.objects.all()
        all_data = [{'SpecialKey': item.SpecialKey, 'Key': chr(int(item.Key)), 'KeyCode': item.Key, 'Message': item.Message} \
                    for item in data_query_set]
        key_mapping_dict = {}
        for item in data_query_set:
            key_mapping_dict['%s_%s' % (item.SpecialKey, item.Key)] = {'Message': item.Message, 
                                                                       'SpecialKey': item.SpecialKey, 
                                                                       'Key': item.Key, 
                                                                       'KeyText': chr(int(item.Key))}
        key_mapping_json = json.dumps(key_mapping_dict)
        keys = [(item, chr(item)) for item in range(ord('A'), ord('Z') + 1)]
        return {'key_mapping': all_data,
                'key_mapping_json': key_mapping_json,
                'keys': keys,
                'special_keys': SPECIAL_KEYS}
    
class HomeAjaxView(BaseJsonAjaxView):
    
    def input_definition(self, request, *args, **kwargs):
        oper = request.POST.get('oper')
        special_key = request.POST.get('special_key', '')
        key = request.POST.get('key', '')
        
        if oper == 'edit':
            rt = {'Code': 1, 'Message': 'Definition created successfully!'}
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
                key_mapping = KeyMapping.objects.get_or_create(SpecialKey=special_key, Key=key)
                if key_mapping[1] == False:
                    rt['Message'] = 'Definition updated successfully!'
                key_mapping = key_mapping[0]
                key_mapping.Message = message
                key_mapping.save()
        elif oper == 'del':
            key_mapping = KeyMapping.objects.filter(SpecialKey=special_key, Key=key)
            key_mapping.delete()
            rt = {'Code': 1, 'Message': 'Definition deleted successfully!'}
        
        return rt
    
    def actions(self):
        handlers = {'input-definition': self.input_definition}
        return handlers
