# -*- coding: utf-8 -*-
import httplib2
import simplejson
from httplib2 import DEFAULT_MAX_REDIRECTS
import urllib

class ApiHandler():
    @staticmethod
    def call_restful_request(url, method, get_params={}, body={}):
        if not url.startswith('http'):
            url = 'http://' + url
        h = httplib2.Http()
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=UTF-8'
        }
        if url.find('?') > 0:
            url += '?a=1'
        params = urllib.urlencode(get_params)
        url += '&' + params
        response, content = h.request(url, method, simplejson.dumps(body), headers, DEFAULT_MAX_REDIRECTS)
        return response, content
    
    @staticmethod
    def call_json(url, method, get_params={}, body={}):
        _, content = ApiHandler.call_restful_request(url, method, get_params, body)
        content = simplejson.loads(content)
        return content
    
if __name__=='__main__':
    ApiHandler.call_restful_request('127.0.0.1:8000/json/sample1/', 'GET', {'param1': 'value1'}, {'body1': 'body value 1'})