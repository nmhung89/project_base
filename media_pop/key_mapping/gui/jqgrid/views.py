from media_pop.common.base_view import BaseTemplateView, BaseJsonAjaxView
from media_pop.key_mapping.core.models import KeyMapping, SPECIAL_KEYS
import simplejson
from cgi import escape

class HomeJqgridView(BaseTemplateView):
    template_name = 'home_jqgrid.html'
    
    def get_data(self):
        data_query_set = KeyMapping.objects.all()
        key_mapping_dict = {}
        for item in data_query_set:
            key_mapping_dict['%s_%s' % (item.SpecialKey, item.Key)] = {'Message': item.Message, 
                                                                       'SpecialKey': item.SpecialKey, 
                                                                       'Key': item.Key, 
                                                                       'KeyText': chr(item.Key)}
        key_mapping_json = simplejson.dumps(key_mapping_dict)
        key_options = ''
        special_key_options = ''
        for item in range(ord('A'), ord('Z') + 1):
            key_options += str(item) + ':' + chr(item) + ';'
        key_options = key_options[:-1]
        for item in SPECIAL_KEYS:
            special_key_options += item[0] + ':' + item[1] + ';'
        special_key_options = special_key_options[:-1]
        return {
                'key_mapping_json': key_mapping_json,
                'keys': key_options,
                'special_keys': special_key_options}
    
class HomeJqgridAjaxView(BaseJsonAjaxView):
    
    def load_grid_data(self, request, *args, **kwargs):
        page = int(request.GET.get('page', 1))
        num = int(request.GET.get('rows', 10))
        sidx = request.GET.get('sidx', '')
        sord = request.GET.get('sord', '')
        sord = '' if sord == 'asc' else '-'
        sord = sord + sidx
        total = KeyMapping.objects.all().count()
        data = KeyMapping.objects.all().order_by('SpecialKey')
        if sidx:
            data = data.order_by(sord)
            
        data = data[((page-1)*num):(page*num)]
        rows = []
        for item in data:
            rows.append({'id': item.pk,
                         'cell': [item.SpecialKey, chr(item.Key), escape(item.Message)]
                         })
        return {"page": page,
                "total": total/num + 1,
                "records": total,
                "rows": rows
                }
    
    def edit_grid_data(self, request, *args, **kwargs):
        oper = request.POST['oper']
        if oper == 'add':
            rt = {'Code': 1, 'Message': 'Definition created successfully!'}
            special_key = request.POST['SpecialKey']
            key = request.POST['Key']
            message = request.POST['Message']
            if not special_key or not key or not message:
                rt['Code'] = -1
                if not special_key:
                    rt['Message'] = 'Please select special key'
                if not key:
                    rt['Message'] = 'Please select key'
                if not message:
                    rt['Message'] = 'Please enter message'
            else:
                chk = KeyMapping.objects.filter(SpecialKey=special_key, Key=key).exists()
                if chk:
                    rt['Code'] = -1
                    rt['Message'] = 'Your keys have been existed!'
                else:
                    key_mapping = KeyMapping(SpecialKey=special_key, Key=key, Message=message)
                    key_mapping.save()
        elif oper == 'edit':
            rt = {'Code': 1, 'Message': 'Definition updated successfully!'}
            message = request.POST['Message']
            pk = request.POST['id']
            if not message:
                rt['Code'] = -1
                rt['Message'] = 'Please enter message'
            else:
                key_mapping = KeyMapping.objects.get(pk=pk)
                key_mapping.Message = message
                key_mapping.save()
        elif oper == 'del':
            rt = {'Code': 1, 'Message': 'Definition deleted successfully!'}
            pk = request.POST['id']
            key_mapping = KeyMapping.objects.get(pk=pk)
            key_mapping.delete()
        return rt
    
    def actions(self):
        handlers = {'load-grid-data': self.load_grid_data,
                    'edit-grid-data': self.edit_grid_data}
        return handlers
