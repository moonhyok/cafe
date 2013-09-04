from django.http import HttpResponse
from django.core import serializers
try:
    import json
except ImportError:
    import simplejson as json

# Wrapper around the lengthy simplejson.dumps call.
def serialize(object, *args, **kwargs):
    return json.dumps(object)

def decode_string(string):
    return json.loads(string)
    
# Returns an error in JSON format
def json_error(error):
    return HttpResponse(serialize({'error': error}))

# Returns a success in JSON format
def json_success():
    return HttpResponse(serialize({'success': True}))

# Returns a result (passed as a dictionary) in JSON format
def json_result(result):
    return HttpResponse(serialize(result, ensure_ascii=True))
